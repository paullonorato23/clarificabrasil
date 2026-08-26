"""Testes das regras de moderação colaborativa.

Regra central: uma promessa pendente é publicada após 3 validações da
comunidade ou pela aprovação direta de um moderador.
"""

from sqlalchemy import select

from app.enums import SituacaoModeracao
from app.models import Usuario
from tests.conftest import auth_header, nova_promessa, registrar_e_logar


def _fila(client, token):
    resp = client.get("/moderacao/promessas", headers=auth_header(token))
    assert resp.status_code == 200
    return resp.json()


def test_fila_lista_pendentes_com_contagens(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    nova_promessa(db, parlamentar.id, autor_id)

    item = _fila(client, token_usuario)[0]
    assert item["parlamentarId"] == parlamentar.id
    assert item["validacoes"] == 0
    assert item["questionamentos"] == 0
    assert item["enviadaPor"] == "Usuária Comum"


def test_fila_exige_autenticacao(client):
    assert client.get("/moderacao/promessas").status_code == 401


def test_tres_validacoes_publicam(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)

    for i in range(3):
        token = registrar_e_logar(client, f"validador{i}@teste.org")
        resp = client.post(
            f"/moderacao/promessas/{promessa.id}/validar", headers=auth_header(token)
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["validacoes"] == i + 1

    db.refresh(promessa)
    assert promessa.situacao == SituacaoModeracao.PUBLICADA

    # A promessa publicada passa a aparecer no perfil público do parlamentar.
    perfil = client.get(f"/parlamentares/{parlamentar.id}").json()
    assert len(perfil["promessas"]) == 1


def test_autor_nao_valida_a_propria_promessa(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)

    for acao in ("validar", "questionar"):
        resp = client.post(
            f"/moderacao/promessas/{promessa.id}/{acao}", headers=auth_header(token_usuario)
        )
        assert resp.status_code == 403


def test_validacao_duplicada_retorna_409(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)
    token = registrar_e_logar(client, "validador@teste.org")

    assert client.post(f"/moderacao/promessas/{promessa.id}/validar", headers=auth_header(token)).status_code == 200
    assert client.post(f"/moderacao/promessas/{promessa.id}/validar", headers=auth_header(token)).status_code == 409


def test_questionar_nao_publica(client, db, parlamentar, token_usuario):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)

    for i in range(3):
        token = registrar_e_logar(client, f"critico{i}@teste.org")
        resp = client.post(
            f"/moderacao/promessas/{promessa.id}/questionar", headers=auth_header(token)
        )
        assert resp.status_code == 200

    db.refresh(promessa)
    assert promessa.situacao == SituacaoModeracao.PENDENTE


def test_moderar_promessa_inexistente_retorna_404(client, token_usuario):
    resp = client.post(
        "/moderacao/promessas/nao-existe/validar", headers=auth_header(token_usuario)
    )
    assert resp.status_code == 404


def test_usuario_comum_nao_aprova_nem_rejeita(client, db, parlamentar, token_usuario):
    registrar_e_logar(client, "autor@teste.org")
    autor = db.scalar(select(Usuario).where(Usuario.email == "autor@teste.org"))
    promessa = nova_promessa(db, parlamentar.id, autor.id)

    assert client.post(f"/moderacao/promessas/{promessa.id}/aprovar", headers=auth_header(token_usuario)).status_code == 403
    assert client.post(
        f"/moderacao/promessas/{promessa.id}/rejeitar",
        json={"motivo": "fonte inválida"},
        headers=auth_header(token_usuario),
    ).status_code == 403


def test_moderador_aprova(client, db, parlamentar, token_usuario, token_moderador):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)

    resp = client.post(
        f"/moderacao/promessas/{promessa.id}/aprovar", headers=auth_header(token_moderador)
    )
    assert resp.status_code == 200
    db.refresh(promessa)
    assert promessa.situacao == SituacaoModeracao.PUBLICADA


def test_moderador_rejeita_exige_motivo(client, db, parlamentar, token_usuario, token_moderador):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)

    assert client.post(
        f"/moderacao/promessas/{promessa.id}/rejeitar", json={}, headers=auth_header(token_moderador)
    ).status_code == 422

    resp = client.post(
        f"/moderacao/promessas/{promessa.id}/rejeitar",
        json={"motivo": "Fonte é página de humor/sátira."},
        headers=auth_header(token_moderador),
    )
    assert resp.status_code == 200
    db.refresh(promessa)
    assert promessa.situacao == SituacaoModeracao.REJEITADA
    assert promessa.motivo_rejeicao == "Fonte é página de humor/sátira."


def test_promessa_ja_moderada_sai_da_fila(client, db, parlamentar, token_usuario, token_moderador):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    promessa = nova_promessa(db, parlamentar.id, autor_id)

    client.post(f"/moderacao/promessas/{promessa.id}/aprovar", headers=auth_header(token_moderador))

    assert _fila(client, token_usuario) == []
    # E não pode mais ser validada.
    token = registrar_e_logar(client, "tardio@teste.org")
    assert client.post(
        f"/moderacao/promessas/{promessa.id}/validar", headers=auth_header(token)
    ).status_code == 404


def test_moderador_nao_modera_o_proprio_envio(
    client, db, parlamentar, moderador, token_moderador
):
    """Nem moderadores podem aprovar/rejeitar promessas que eles mesmos enviaram."""
    promessa = nova_promessa(db, parlamentar.id, moderador.id)

    assert client.post(
        f"/moderacao/promessas/{promessa.id}/aprovar", headers=auth_header(token_moderador)
    ).status_code == 403
    assert client.post(
        f"/moderacao/promessas/{promessa.id}/rejeitar",
        json={"motivo": "qualquer"},
        headers=auth_header(token_moderador),
    ).status_code == 403

    db.refresh(promessa)
    assert promessa.situacao == SituacaoModeracao.PENDENTE


def test_outro_moderador_consegue_moderar(client, db, parlamentar, moderador, token_moderador):
    """A promessa de um moderador pode ser moderada por OUTRO moderador."""
    from app.enums import PapelUsuario
    from app.security import hash_senha

    outro = Usuario(
        nome="Moderador 2",
        email="mod2@teste.org",
        senha_hash=hash_senha("senha-segura"),
        papel=PapelUsuario.MODERADOR,
    )
    db.add(outro)
    db.commit()

    promessa = nova_promessa(db, parlamentar.id, moderador.id)

    resp_login = client.post(
        "/auth/login", json={"email": "mod2@teste.org", "senha": "senha-segura"}
    )
    token_mod2 = resp_login.json()["accessToken"]

    resp = client.post(
        f"/moderacao/promessas/{promessa.id}/aprovar", headers=auth_header(token_mod2)
    )
    assert resp.status_code == 200
    db.refresh(promessa)
    assert promessa.situacao == SituacaoModeracao.PUBLICADA
