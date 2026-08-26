"""Testes dos endpoints públicos de parlamentares e ranking."""

from datetime import date

from app.enums import SituacaoModeracao, StatusPromessa, StatusProposicao, Tema, TipoProposicao, VotoNominal
from app.models import Gasto, Proposicao, Votacao
from tests.conftest import nova_promessa, registrar_e_logar


def _popular(db, parlamentar, autor_id):
    """Uma promessa publicada, uma pendente, uma proposição, uma votação e um gasto."""
    nova_promessa(
        db, parlamentar.id, autor_id,
        situacao=SituacaoModeracao.PUBLICADA, status=StatusPromessa.CUMPRIDA,
    )
    nova_promessa(
        db, parlamentar.id, autor_id,
        situacao=SituacaoModeracao.PENDENTE, texto="Promessa ainda em moderação",
    )
    db.add(Proposicao(
        parlamentar_id=parlamentar.id, tipo=TipoProposicao.PL, numero="1452/2023",
        ementa="Dispõe sobre...", tema=Tema.EDUCACAO,
        status=StatusProposicao.EM_TRAMITACAO, data=date(2023, 3, 1),
    ))
    db.add(Votacao(
        parlamentar_id=parlamentar.id, materia="PL 1452/2023", tema=Tema.EDUCACAO,
        data=date(2023, 5, 20), voto=VotoNominal.SIM, coerente_com_discurso=True,
    ))
    db.add(Gasto(parlamentar_id=parlamentar.id, categoria="Passagens aéreas", valor=12345.0, ano=2024))
    db.commit()


def test_listar_vazio(client):
    assert client.get("/parlamentares").json() == []


def test_listar_com_filtros(client, db, parlamentar):
    assert len(client.get("/parlamentares").json()) == 1
    assert len(client.get("/parlamentares", params={"casa": "camara"}).json()) == 1
    assert client.get("/parlamentares", params={"casa": "senado"}).json() == []
    assert client.get("/parlamentares", params={"uf": "rj"}).json() == []
    assert len(client.get("/parlamentares", params={"busca": "beatriz"}).json()) == 1
    assert client.get("/parlamentares", params={"partido": "outro"}).json() == []


def test_detalhe_retorna_dados_e_score(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers={"Authorization": f"Bearer {token_usuario}"}).json()["id"]
    _popular(db, parlamentar, autor_id)

    resp = client.get(f"/parlamentares/{parlamentar.id}")
    assert resp.status_code == 200
    corpo = resp.json()

    assert corpo["nome"] == "Ana Beatriz Ramos"
    # Score: promessa cumprida (1.0) + voto coerente (1.0) → 0.7*1 + 0.3*1 = 100
    assert corpo["score"] == 100
    assert corpo["resumoPromessas"]["cumprida"] == 1
    assert len(corpo["proposicoes"]) == 1
    assert len(corpo["votacoes"]) == 1
    assert corpo["gastos"][0]["categoria"] == "Passagens aéreas"


def test_detalhe_nao_expoe_promessas_pendentes(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers={"Authorization": f"Bearer {token_usuario}"}).json()["id"]
    _popular(db, parlamentar, autor_id)

    corpo = client.get(f"/parlamentares/{parlamentar.id}").json()
    textos = [p["texto"] for p in corpo["promessas"]]
    assert "Promessa ainda em moderação" not in textos
    assert len(corpo["promessas"]) == 1


def test_detalhe_incrementa_acessos(client, parlamentar):
    antes = client.get(f"/parlamentares/{parlamentar.id}").json()["acessos"]
    depois = client.get(f"/parlamentares/{parlamentar.id}").json()["acessos"]
    assert depois == antes + 1


def test_detalhe_inexistente_retorna_404(client):
    assert client.get("/parlamentares/ninguem").status_code == 404


def test_ranking_por_acessos(client, db, parlamentar):
    corpo = client.get("/ranking").json()
    assert corpo[0]["id"] == parlamentar.id
    assert corpo[0]["acessos"] == 100


def test_ranking_por_score(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers={"Authorization": f"Bearer {token_usuario}"}).json()["id"]
    _popular(db, parlamentar, autor_id)

    corpo = client.get("/ranking", params={"por": "score"}).json()
    assert corpo[0]["score"] == 100


def test_ranking_parametro_invalido_retorna_422(client):
    assert client.get("/ranking", params={"por": "banana"}).status_code == 422
