"""Testes do Score de Coerência v0.1 — fórmula idêntica à do frontend."""

from types import SimpleNamespace

from app.score import (
    PESO_PROMESSAS,
    PESO_VOTOS,
    calcular_score,
    percentual_entrega,
    percentual_votos_coerentes,
    resumo_promessas,
)


def promessa(status: str):
    return SimpleNamespace(status=status)


def votacao(coerente: bool):
    return SimpleNamespace(coerente_com_discurso=coerente)


def test_pesos_batem_com_frontend():
    assert PESO_PROMESSAS == 0.7
    assert PESO_VOTOS == 0.3


def test_score_sem_dados_e_zero():
    assert calcular_score([], []) == 0


def test_score_so_promessas_assume_peso_total():
    # média = (1 + 0) / 2 = 0.5 → 50
    assert calcular_score([promessa("cumprida"), promessa("contraditada")], []) == 50


def test_score_so_votacoes_assume_peso_total():
    assert calcular_score([], [votacao(True), votacao(False)]) == 50


def test_score_combina_70_30():
    # promessas: média 1.0; votos: 1/2 = 0.5 → 0.7*1 + 0.3*0.5 = 0.85 → 85
    promessas = [promessa("cumprida")]
    votacoes = [votacao(True), votacao(False)]
    assert calcular_score(promessas, votacoes) == 85


def test_pontos_intermediarios():
    # em_andamento=0.5, sem_acao=0.25 → média 0.375; sem votos → peso total → 37.5 → 38 (round)
    assert calcular_score([promessa("em_andamento"), promessa("sem_acao")], []) == 38


def test_resumo_promessas():
    promessas = [
        promessa("cumprida"),
        promessa("cumprida"),
        promessa("em_andamento"),
        promessa("contraditada"),
    ]
    assert resumo_promessas(promessas) == {
        "cumprida": 2,
        "em_andamento": 1,
        "contraditada": 1,
        "sem_acao": 0,
    }


def test_percentual_entrega():
    assert percentual_entrega([]) == 0
    assert percentual_entrega([promessa("cumprida"), promessa("sem_acao")]) == 50


def test_percentual_votos_coerentes():
    assert percentual_votos_coerentes([]) == 0
    votacoes = [votacao(True), votacao(True), votacao(False)]
    assert percentual_votos_coerentes(votacoes) == 67


def test_votos_nao_avaliados_sao_ignorados():
    """Votos importados sem avaliação editorial (None) não entram no cálculo."""
    # Só votos não avaliados → como se não houvesse votos: promessas assumem peso total.
    assert calcular_score([promessa("cumprida")], [votacao(None)]) == 100
    # Mistura: a média de votos considera apenas os avaliados (1/1 = 1.0).
    assert calcular_score([promessa("contraditada")], [votacao(True), votacao(None)]) == 30
    assert percentual_votos_coerentes([votacao(None), votacao(True)]) == 100
    assert percentual_votos_coerentes([votacao(None)]) == 0
