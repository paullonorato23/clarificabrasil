"""Testes da integração com a API da Câmara (issue #8).

Toda a comunicação HTTP é mockada com httpx.MockTransport — nenhum teste
acessa a rede.
"""

from datetime import date

import httpx
import pytest
from sqlalchemy import select

from app.enums import Casa, StatusProposicao, TipoProposicao, VotoNominal
from app.integracoes.camara import CamaraClient
from app.integracoes.sincronizacao import (
    mapear_status_proposicao,
    mapear_voto,
    sincronizar_deputados,
    sincronizar_despesas,
    sincronizar_proposicoes,
    sincronizar_votacoes,
    slugify,
)
from app.models import Gasto, Parlamentar, Proposicao, Votacao

# ------------------------------------------------------------ massa fake

DEPUTADO = {"id": 204554, "nome": "Ana Beatriz Ramos", "siglaPartido": "PXX", "siglaUf": "SP"}
LEGISLATURA = {"id": 57, "dataInicio": "2023-02-01", "dataFim": "2027-01-31"}

PROPOSICAO_PL = {
    "id": 2300001, "siglaTipo": "PL", "numero": 1452, "ano": 2023,
    "ementa": "Dispõe sobre a criação de creches", "dataApresentacao": "2023-03-01T10:00:00",
}
PROPOSICAO_MPV = {
    "id": 2300002, "siglaTipo": "MPV", "numero": 999, "ano": 2023,
    "ementa": "Medida provisória fora do escopo", "dataApresentacao": "2023-04-01T10:00:00",
}
DETALHE_PL = {**PROPOSICAO_PL, "statusProposicao": {"descricaoSituacao": "Pronta para Pauta"}}

VOTACAO = {"id": "2456789-123", "dataHoraRegistro": "2026-08-20T15:30:00", "descricao": "PL 1452/2023"}
VOTOS = [
    {"tipoVoto": "Sim", "deputado_": {"id": 204554, "nome": "Ana Beatriz Ramos"}},
    {"tipoVoto": "Não votou", "deputado_": {"id": 204554, "nome": "Ana Beatriz Ramos"}},
    {"tipoVoto": "Sim", "deputado_": {"id": 999999, "nome": "Desconhecido"}},
]

DESPESAS = [
    {"ano": 2026, "mes": 1, "tipoDespesa": "PASSAGENS AÉREAS", "valorLiquido": 1000.0},
    {"ano": 2026, "mes": 2, "tipoDespesa": "PASSAGENS AÉREAS", "valorLiquido": 500.5},
    {"ano": 2026, "mes": 2, "tipoDespesa": "COMBUSTÍVEIS E LUBRIFICANTES", "valorLiquido": 300.0},
]


def _resposta(dados, tem_proxima=False):
    links = [{"rel": "next", "href": "https://teste/next"}] if tem_proxima else []
    return httpx.Response(200, json={"dados": dados, "links": links})


def handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    pagina = int(request.url.params.get("pagina", "1"))

    if path.endswith("/legislaturas"):
        return _resposta([LEGISLATURA])
    if path.endswith("/deputados") and "despesas" not in path:
        if pagina == 1:
            return _resposta([DEPUTADO], tem_proxima=True)
        return _resposta([{**DEPUTADO, "id": 204555, "nome": "Carlos Souza", "siglaUf": "RJ"}])
    if path.endswith("/proposicoes"):
        return _resposta([PROPOSICAO_PL, PROPOSICAO_MPV])
    if "/proposicoes/" in path:
        return httpx.Response(200, json={"dados": DETALHE_PL})
    if path.endswith("/votos"):
        return _resposta(VOTOS)
    if path.endswith("/votacoes"):
        return _resposta([VOTACAO])
    if path.endswith("/despesas"):
        return _resposta(DESPESAS)
    return httpx.Response(404, json={"erro": "não encontrado"})


@pytest.fixture()
def cliente():
    with CamaraClient(base_url="https://teste/api/v2", transport=httpx.MockTransport(handler)) as c:
        yield c


# --------------------------------------------------------------- cliente

def test_paginacao_percorre_todas_as_paginas(cliente):
    deputados = cliente.listar_deputados()
    assert len(deputados) == 2
    assert deputados[0]["nome"] == "Ana Beatriz Ramos"


# ------------------------------------------------------- mapeamentos

def test_slugify():
    assert slugify("Ana Beatriz Ramos") == "ana-beatriz-ramos"
    assert slugify("José Ênio Çandio") == "jose-enio-candio"


def test_mapear_status_proposicao():
    assert mapear_status_proposicao("Arquivada") == StatusProposicao.ARQUIVADA
    assert mapear_status_proposicao("Transformada em Lei") == StatusProposicao.SANCIONADA
    assert mapear_status_proposicao("Aprovada") == StatusProposicao.APROVADA
    assert mapear_status_proposicao("Pronta para Pauta") == StatusProposicao.EM_TRAMITACAO
    assert mapear_status_proposicao(None) == StatusProposicao.EM_TRAMITACAO


def test_mapear_voto():
    assert mapear_voto("Sim") == VotoNominal.SIM
    assert mapear_voto("Não") == VotoNominal.NAO
    assert mapear_voto("Abstenção") == VotoNominal.ABSTENCAO
    assert mapear_voto("Não votou") == VotoNominal.AUSENTE
    assert mapear_voto("Obstrução") == VotoNominal.AUSENTE
    assert mapear_voto(None) == VotoNominal.AUSENTE


# ------------------------------------------------------------ deputados

def test_sincronizar_deputados_cria_e_atualiza(db, cliente):
    total = sincronizar_deputados(db, cliente)
    assert total == 2

    ana = db.scalar(select(Parlamentar).where(Parlamentar.id_camara == 204554))
    assert ana.id == "ana-beatriz-ramos"
    assert ana.casa == Casa.CAMARA
    assert ana.partido == "PXX"
    assert ana.uf == "SP"
    assert ana.mandato == "2023–2027"

    # Roda de novo: atualiza, não duplica.
    total2 = sincronizar_deputados(db, cliente)
    assert total2 == 2
    assert db.scalar(select(Parlamentar).where(Parlamentar.id_camara == 204554)).id == "ana-beatriz-ramos"
    assert len(db.scalars(select(Parlamentar)).all()) == 2


# ---------------------------------------------------------- proposições

def test_sincronizar_proposicoes_filtra_tipos_e_mapeia(db, cliente):
    sincronizar_deputados(db, cliente)
    total = sincronizar_proposicoes(db, cliente)

    # A MPV é ignorada; só o PL entra (para cada deputado a API devolve a mesma lista,
    # mas o upsert por id_camara impede duplicatas).
    proposicoes = db.scalars(select(Proposicao)).all()
    assert len(proposicoes) == 1

    prop = proposicoes[0]
    assert prop.id_camara == 2300001
    assert prop.tipo == TipoProposicao.PL
    assert prop.numero == "1452/2023"
    assert prop.status == StatusProposicao.EM_TRAMITACAO
    assert prop.tema is None
    assert prop.data == date(2023, 3, 1)
    assert total >= 1


# ------------------------------------------------------------- votações

def test_sincronizar_votacoes_importa_apenas_conhecidos(db, cliente, monkeypatch):
    sincronizar_deputados(db, cliente)

    # Fixa a janela para incluir a data da votação fake.
    monkeypatch.setattr("app.integracoes.sincronizacao.date", _DataFixa)
    total = sincronizar_votacoes(db, cliente, dias=30)

    votacoes = db.scalars(select(Votacao)).all()
    # O deputado 999999 não está no banco → ignorado. Para a Ana há 2 registros
    # na lista fake, mas o upsert por (id_camara, parlamentar) consolida em 1.
    assert len(votacoes) == 1
    v = votacoes[0]
    assert v.id_camara == "2456789-123"
    assert v.materia == "PL 1452/2023"
    assert v.data == date(2026, 8, 20)
    assert v.voto == VotoNominal.AUSENTE  # último registro da lista ("Não votou")
    assert v.coerente_com_discurso is None
    assert v.tema is None


class _DataFixa(date):
    @classmethod
    def today(cls):
        return cls(2026, 8, 27)


# -------------------------------------------------------------- despesas

def test_sincronizar_despesas_agrega_por_categoria(db, cliente):
    sincronizar_deputados(db, cliente)
    sincronizar_despesas(db, cliente, ano=2026)

    gastos = db.scalars(select(Gasto)).all()
    por_categoria = {g.categoria: g.valor for g in gastos}
    assert por_categoria["PASSAGENS AÉREAS"] == 1500.5
    assert por_categoria["COMBUSTÍVEIS E LUBRIFICANTES"] == 300.0
    assert all(g.ano == 2026 for g in gastos)


def test_sincronizar_despesas_substitui_sem_duplicar(db, cliente):
    sincronizar_deputados(db, cliente)
    sincronizar_despesas(db, cliente, ano=2026)
    sincronizar_despesas(db, cliente, ano=2026)

    gastos = db.scalars(select(Gasto)).all()
    assert len([g for g in gastos if g.categoria == "PASSAGENS AÉREAS"]) == 2  # um por deputado
