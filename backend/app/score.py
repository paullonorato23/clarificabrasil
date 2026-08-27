"""Score de Coerência — versão 0.1.

A metodologia é pública e auditável (ver a rota /metodologia do frontend e
`frontend/src/lib/score.ts`, que este módulo espelha). Qualquer mudança nesta
fórmula deve ser documentada e versionada neste repositório.

Cálculo: 70% vem das promessas de campanha e 30% das votações nominais.
Se uma das fontes estiver vazia, a outra assume peso total.

Esclarecimento da v0.1 (27/08/2026): votos importados das APIs oficiais ainda
não têm avaliação editorial de coerência (`coerente_com_discurso = None`).
Votos não avaliados são **ignorados** no cálculo — a média considera apenas
votos avaliados (True/False). Se nenhum voto foi avaliado, as promessas
assumem peso total.

As funções aceitam qualquer objeto com os atributos esperados (modelos
SQLAlchemy ou namespaces de teste); o status pode ser o enum ou a string.
"""

from __future__ import annotations

from typing import Dict, Sequence

PESO_PROMESSAS = 0.7
PESO_VOTOS = 0.3

# Pontos atribuídos a cada situação de promessa, de 0 a 1.
PONTOS_POR_STATUS: Dict[str, float] = {
    "cumprida": 1.0,
    "em_andamento": 0.5,
    "sem_acao": 0.25,
    "contraditada": 0.0,
}


def _valor(obj) -> str:
    """Aceita enum (StatusPromessa) ou string e devolve o valor em string."""
    return getattr(obj, "value", obj)


def _votos_avaliados(votacoes: Sequence) -> list:
    """Votos com avaliação editorial de coerência (ignora os não avaliados)."""
    return [v for v in votacoes if v.coerente_com_discurso is not None]


def calcular_score(promessas: Sequence, votacoes: Sequence) -> int:
    media_promessas = (
        sum(PONTOS_POR_STATUS[_valor(p.status)] for p in promessas) / len(promessas)
        if promessas
        else None
    )
    avaliados = _votos_avaliados(votacoes)
    media_votos = (
        sum(1 for v in avaliados if v.coerente_com_discurso) / len(avaliados)
        if avaliados
        else None
    )

    if media_promessas is None and media_votos is None:
        return 0

    peso_promessas = 0 if media_promessas is None else (1 if media_votos is None else PESO_PROMESSAS)
    peso_votos = 0 if media_votos is None else (1 if media_promessas is None else PESO_VOTOS)

    return round((peso_promessas * (media_promessas or 0) + peso_votos * (media_votos or 0)) * 100)


def resumo_promessas(promessas: Sequence) -> Dict[str, int]:
    """Contagem de promessas por status, usada no perfil e no comparador."""
    resumo = {status: 0 for status in PONTOS_POR_STATUS}
    for p in promessas:
        resumo[_valor(p.status)] += 1
    return resumo


def percentual_entrega(promessas: Sequence) -> int:
    """Percentual de promessas com status cumprida."""
    if not promessas:
        return 0
    cumpridas = sum(1 for p in promessas if _valor(p.status) == "cumprida")
    return round(cumpridas / len(promessas) * 100)


def percentual_votos_coerentes(votacoes: Sequence) -> int:
    """Percentual (0–100) de votos coerentes entre os votos avaliados."""
    avaliados = _votos_avaliados(votacoes)
    if not avaliados:
        return 0
    coerentes = sum(1 for v in avaliados if v.coerente_com_discurso)
    return round(coerentes / len(avaliados) * 100)
