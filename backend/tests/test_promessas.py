"""Testes do cadastro colaborativo de promessas, incluindo a verificação
automática do link da fonte (mockada — os testes não acessam a rede)."""

import app.fontes
from tests.conftest import auth_header, dados_promessa


def test_criar_sem_token_retorna_401(client, parlamentar):
    resp = client.post("/promessas", json=dados_promessa(parlamentar.id))
    assert resp.status_code == 401


def test_criar_url_invalida_retorna_422(client, parlamentar, token_usuario):
    dados = dados_promessa(parlamentar.id)
    dados["fonteUrl"] = "nao-e-uma-url"
    resp = client.post("/promessas", json=dados, headers=auth_header(token_usuario))
    assert resp.status_code == 422


def test_criar_parlamentar_inexistente_retorna_404(client, token_usuario):
    resp = client.post(
        "/promessas", json=dados_promessa("ninguem"), headers=auth_header(token_usuario)
    )
    assert resp.status_code == 404


def test_criar_com_fonte_verificada(client, parlamentar, token_usuario, monkeypatch):
    monkeypatch.setattr(app.fontes, "verificar_fonte", lambda url, timeout=5.0: (True, 200))

    resp = client.post(
        "/promessas",
        json=dados_promessa(parlamentar.id),
        headers=auth_header(token_usuario),
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["situacao"] == "pendente"
    assert corpo["status"] == "sem_acao"
    assert corpo["fonteVerificada"] is True
    assert corpo["fonteStatusHttp"] == 200
    assert corpo["fonteUrl"] == "https://exemplo.org/entrevista"  # camelCase


def test_criar_com_link_quebrado_marca_nao_verificada(
    client, parlamentar, token_usuario, monkeypatch
):
    monkeypatch.setattr(app.fontes, "verificar_fonte", lambda url, timeout=5.0: (False, 404))

    resp = client.post(
        "/promessas",
        json=dados_promessa(parlamentar.id),
        headers=auth_header(token_usuario),
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["fonteVerificada"] is False
    assert corpo["fonteStatusHttp"] == 404


def test_criar_com_fonte_sem_resposta_marca_nao_verificada(
    client, parlamentar, token_usuario, monkeypatch
):
    monkeypatch.setattr(app.fontes, "verificar_fonte", lambda url, timeout=5.0: (False, None))

    resp = client.post(
        "/promessas",
        json=dados_promessa(parlamentar.id),
        headers=auth_header(token_usuario),
    )
    assert resp.status_code == 201
    assert resp.json()["fonteVerificada"] is False
    assert resp.json()["fonteStatusHttp"] is None


def test_obter_pendente_restrita_a_autor_e_moderador(
    client, db, parlamentar, token_usuario, token_moderador
):
    autor_id = client.get("/auth/me", headers=auth_header(token_usuario)).json()["id"]
    from tests.conftest import nova_promessa, registrar_e_logar

    promessa = nova_promessa(db, parlamentar.id, autor_id)
    outro = registrar_e_logar(client, "outro@teste.org")

    assert client.get(f"/promessas/{promessa.id}").status_code == 403
    assert client.get(f"/promessas/{promessa.id}", headers=auth_header(outro)).status_code == 403
    assert client.get(f"/promessas/{promessa.id}", headers=auth_header(token_usuario)).status_code == 200
    assert client.get(f"/promessas/{promessa.id}", headers=auth_header(token_moderador)).status_code == 200


def test_obter_inexistente_retorna_404(client):
    assert client.get("/promessas/nao-existe").status_code == 404
