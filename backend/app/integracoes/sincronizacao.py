"""Sincronização dos dados oficiais da Câmara com o nosso banco (issue #8).

Uso via CLI (a partir de backend/):

    python -m app.integracoes.sincronizacao --etapa deputados
    python -m app.integracoes.sincronizacao --etapa tudo --dias 30 --ano 2026

Todas as etapas são idempotentes: usam os IDs oficiais da Câmara
(`id_camara`) para atualizar registros existentes em vez de duplicar.

Decisões de mapeamento (detalhadas em Docs/Doubts.md, itens 13 a 15):
- Apenas PL, PEC e REQ são importados (o enum do frontend só tem esses tipos);
- `tema` fica nulo até a categorização automática (issue #28);
- coerência com o discurso fica nula (avaliação editorial, não vem da API);
- votos que não são Sim/Não/Abstenção viram Ausente.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.enums import Casa, StatusProposicao, TipoProposicao, VotoNominal
from app.integracoes.camara import CamaraClient
from app.models import Gasto, Parlamentar, Proposicao, Votacao

# Somente os tipos que o frontend conhece (ver Docs/Doubts.md, item 13).
TIPOS_IMPORTADOS: Dict[str, TipoProposicao] = {
    "PL": TipoProposicao.PL,
    "PEC": TipoProposicao.PEC,
    "REQ": TipoProposicao.REQ,
}

# Tipo de voto oficial → nosso enum. "Não votou", "Obstrução", "Presente",
# "Branco" etc. indicam ausência de voto efetivo → Ausente (Doubts, item 15).
MAP_VOTO: Dict[str, VotoNominal] = {
    "Sim": VotoNominal.SIM,
    "Não": VotoNominal.NAO,
    "Abstenção": VotoNominal.ABSTENCAO,
}


def slugify(nome: str) -> str:
    """Gera o slug da URL a partir do nome (ex.: "Ana Beatriz Ramos" → "ana-beatriz-ramos")."""
    sem_acento = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", sem_acento.lower()).strip("-")
    return slug or "parlamentar"


def mapear_status_proposicao(descricao: Optional[str]) -> StatusProposicao:
    """Mapeia a situação textual da Câmara para o nosso enum (Doubts, item 14)."""
    texto = (descricao or "").lower()
    if "arquivad" in texto:
        return StatusProposicao.ARQUIVADA
    if "sancion" in texto or "promulg" in texto or "transformad" in texto:
        return StatusProposicao.SANCIONADA
    if "aprovad" in texto:
        return StatusProposicao.APROVADA
    return StatusProposicao.EM_TRAMITACAO


def mapear_voto(tipo_voto: Optional[str]) -> VotoNominal:
    return MAP_VOTO.get(tipo_voto or "", VotoNominal.AUSENTE)


def _data(texto: Optional[str]) -> Optional[date]:
    """Extrai a data (AAAA-MM-DD) de um campo datetime da API."""
    if not texto:
        return None
    return date.fromisoformat(texto[:10])


# ---------------------------------------------------------- deputados

def sincronizar_deputados(db: Session, cliente: CamaraClient) -> int:
    legislatura = cliente.legislatura_atual()
    mandato = f"{_data(legislatura['dataInicio']).year}–{_data(legislatura['dataFim']).year}"

    slugs_em_uso = set(db.scalars(select(Parlamentar.id)).all())
    sincronizados = 0

    for dep in cliente.listar_deputados():
        parlamentar = db.scalar(
            select(Parlamentar).where(Parlamentar.id_camara == dep["id"])
        )
        if parlamentar is None:
            slug = slugify(dep["nome"])
            if slug in slugs_em_uso:
                slug = f"{slug}-{dep['id']}"
            slugs_em_uso.add(slug)
            parlamentar = Parlamentar(id=slug, id_camara=dep["id"], casa=Casa.CAMARA)
            db.add(parlamentar)

        parlamentar.nome = dep["nome"]
        parlamentar.partido = dep["siglaPartido"]
        parlamentar.uf = dep["siglaUf"]
        parlamentar.mandato = mandato
        sincronizados += 1

    db.commit()
    return sincronizados


# -------------------------------------------------------- proposições

def sincronizar_proposicoes(db: Session, cliente: CamaraClient) -> int:
    parlamentares = db.scalars(
        select(Parlamentar).where(Parlamentar.id_camara.is_not(None))
    ).all()
    sincronizadas = 0

    for parlamentar in parlamentares:
        for prop in cliente.listar_proposicoes_autor(parlamentar.id_camara):
            tipo = TIPOS_IMPORTADOS.get(prop["siglaTipo"])
            if tipo is None:
                continue

            detalhe = cliente.detalhe_proposicao(prop["id"])
            situacao = (detalhe.get("statusProposicao") or {}).get("descricaoSituacao")
            data_apresentacao = _data(detalhe.get("dataApresentacao"))
            if data_apresentacao is None:
                continue

            proposicao = db.scalar(
                select(Proposicao).where(Proposicao.id_camara == prop["id"])
            )
            if proposicao is None:
                proposicao = Proposicao(
                    id_camara=prop["id"], parlamentar_id=parlamentar.id
                )
                db.add(proposicao)

            proposicao.tipo = tipo
            proposicao.numero = f"{prop['numero']}/{prop['ano']}"
            proposicao.ementa = prop["ementa"]
            proposicao.tema = None  # categorização automática: issue #28
            proposicao.status = mapear_status_proposicao(situacao)
            proposicao.data = data_apresentacao
            sincronizadas += 1

        db.commit()

    return sincronizadas


# ----------------------------------------------------------- votações

def sincronizar_votacoes(db: Session, cliente: CamaraClient, dias: int = 30) -> int:
    """Importa os votos nominais dos deputados conhecidos nas votações recentes."""
    hoje = date.today()
    votacoes = cliente.listar_votacoes(
        data_inicio=(hoje - timedelta(days=dias)).isoformat(), data_fim=hoje.isoformat()
    )

    # Mapa id oficial → nosso id (só importamos votos de quem já está no banco).
    deputados = {
        p.id_camara: p.id
        for p in db.scalars(
            select(Parlamentar).where(Parlamentar.id_camara.is_not(None))
        )
    }
    sincronizadas = 0

    for votacao in votacoes:
        data_votacao = _data(votacao.get("dataHoraRegistro"))
        if data_votacao is None:
            continue
        materia = (votacao.get("descricao") or "Votação nominal")[:300]

        for voto in cliente.listar_votos(votacao["id"]):
            deputado = voto.get("deputado_") or voto.get("deputado") or {}
            parlamentar_id = deputados.get(deputado.get("id"))
            if parlamentar_id is None:
                continue

            existente = db.scalar(
                select(Votacao).where(
                    Votacao.id_camara == votacao["id"],
                    Votacao.parlamentar_id == parlamentar_id,
                )
            )
            if existente is None:
                existente = Votacao(
                    id_camara=votacao["id"], parlamentar_id=parlamentar_id
                )

            existente.materia = materia
            existente.tema = None  # categorização automática: issue #28
            existente.data = data_votacao
            existente.voto = mapear_voto(voto.get("tipoVoto"))
            # coerente_com_discurso fica None: é avaliação editorial, não vem da API.
            db.add(existente)
            # flush explícito: a sessão usa autoflush=False, e a próxima
            # consulta precisa enxergar este registro (idempotência).
            db.flush()
            sincronizadas += 1

        db.commit()

    return sincronizadas


# ------------------------------------------------------------ despesas

def sincronizar_despesas(db: Session, cliente: CamaraClient, ano: int) -> int:
    """Agrega as despesas de gabinete (CEAP) por categoria e ano."""
    parlamentares = db.scalars(
        select(Parlamentar).where(Parlamentar.id_camara.is_not(None))
    ).all()
    sincronizadas = 0

    for parlamentar in parlamentares:
        totais: Dict[str, float] = {}
        for despesa in cliente.listar_despesas(parlamentar.id_camara, ano):
            categoria = despesa.get("tipoDespesa") or "Outros"
            totais[categoria] = totais.get(categoria, 0.0) + float(
                despesa.get("valorLiquido") or 0
            )

        # Substitui os gastos do ano (idempotente).
        db.execute(
            delete(Gasto).where(Gasto.parlamentar_id == parlamentar.id, Gasto.ano == ano)
        )
        for categoria, valor in sorted(totais.items()):
            db.add(
                Gasto(
                    parlamentar_id=parlamentar.id,
                    categoria=categoria,
                    valor=round(valor, 2),
                    ano=ano,
                )
            )
            sincronizadas += 1

        db.commit()

    return sincronizadas


# ---------------------------------------------------------------- CLI

def main() -> None:
    parser = argparse.ArgumentParser(description="Sincroniza dados oficiais da Câmara.")
    parser.add_argument(
        "--etapa",
        choices=["deputados", "proposicoes", "votacoes", "despesas", "tudo"],
        default="tudo",
    )
    parser.add_argument("--ano", type=int, default=datetime.now().year,
                        help="Ano de referência das despesas")
    parser.add_argument("--dias", type=int, default=30,
                        help="Janela (dias) das votações importadas")
    args = parser.parse_args()

    with CamaraClient() as cliente, SessionLocal() as db:
        if args.etapa in ("deputados", "tudo"):
            print(f"deputados: {sincronizar_deputados(db, cliente)} sincronizados")
        if args.etapa in ("proposicoes", "tudo"):
            print(f"proposições: {sincronizar_proposicoes(db, cliente)} sincronizadas")
        if args.etapa in ("votacoes", "tudo"):
            print(f"votos: {sincronizar_votacoes(db, cliente, dias=args.dias)} sincronizados")
        if args.etapa in ("despesas", "tudo"):
            print(f"gastos: {sincronizar_despesas(db, cliente, ano=args.ano)} categorias sincronizadas")


if __name__ == "__main__":
    main()
