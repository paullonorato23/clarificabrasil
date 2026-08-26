"""Testes de autenticação: registro, login e /auth/me."""

from tests.conftest import auth_header


def test_registro_cria_usuario_comum(client):
    resp = client.post(
        "/auth/registro",
        json={"nome": "Maria Silva", "email": "maria@teste.org", "senha": "senha-segura"},
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["email"] == "maria@teste.org"
    assert corpo["papel"] == "comum"
    assert "senha" not in corpo
    assert "senhaHash" not in corpo


def test_registro_email_duplicado_retorna_409(client):
    dados = {"nome": "Maria Silva", "email": "maria@teste.org", "senha": "senha-segura"}
    assert client.post("/auth/registro", json=dados).status_code == 201
    assert client.post("/auth/registro", json=dados).status_code == 409


def test_registro_senha_curta_retorna_422(client):
    resp = client.post(
        "/auth/registro",
        json={"nome": "Maria Silva", "email": "maria@teste.org", "senha": "curta"},
    )
    assert resp.status_code == 422


def test_login_retorna_token(client, token_usuario):
    assert token_usuario


def test_login_credenciais_invalidas_retorna_401(client, token_usuario):
    resp = client.post(
        "/auth/login", json={"email": "comum@teste.org", "senha": "senha-errada"}
    )
    assert resp.status_code == 401


def test_me_com_token(client, token_usuario):
    resp = client.get("/auth/me", headers=auth_header(token_usuario))
    assert resp.status_code == 200
    assert resp.json()["email"] == "comum@teste.org"


def test_me_sem_token_retorna_401(client):
    # Sem credenciais, a API responde 401 (não autenticado).
    assert client.get("/auth/me").status_code == 401


def test_me_token_invalido_retorna_401(client):
    resp = client.get("/auth/me", headers=auth_header("token-invalido"))
    assert resp.status_code == 401
