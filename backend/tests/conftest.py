"""Fixtures de teste: banco SQLite em memória, client e massas básicas."""

from __future__ import annotations

import os
from datetime import date

# Configura o ambiente ANTES de importar qualquer módulo da app.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "chave-de-teste-com-pelo-menos-32-bytes!!"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.enums import (
    Casa,
    PapelUsuario,
    SituacaoModeracao,
    StatusPromessa,
    StatusProposicao,
    Tema,
    TipoProposicao,
    VotoNominal,
)
from app.models import Gasto, Parlamentar, Promessa, Proposicao, Usuario, Votacao
from app.security import hash_senha
from main import app

engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def db():
    Base.metadata.create_all(engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def registrar_e_logar(client: TestClient, email: str, nome: str = "Usuário Teste") -> str:
    """Registra um usuário comum via API e devolve o token de acesso."""
    resp = client.post(
        "/auth/registro", json={"nome": nome, "email": email, "senha": "senha-segura"}
    )
    assert resp.status_code == 201, resp.text
    resp = client.post("/auth/login", json={"email": email, "senha": "senha-segura"})
    assert resp.status_code == 200, resp.text
    return resp.json()["accessToken"]


@pytest.fixture()
def token_usuario(client):
    return registrar_e_logar(client, "comum@teste.org", "Usuária Comum")


@pytest.fixture()
def moderador(db):
    usuario = Usuario(
        nome="Moderador",
        email="mod@teste.org",
        senha_hash=hash_senha("senha-segura"),
        papel=PapelUsuario.MODERADOR,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture()
def token_moderador(client, moderador):
    resp = client.post(
        "/auth/login", json={"email": "mod@teste.org", "senha": "senha-segura"}
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["accessToken"]


@pytest.fixture()
def parlamentar(db):
    p = Parlamentar(
        id="ana-beatriz-ramos",
        nome="Ana Beatriz Ramos",
        casa=Casa.CAMARA,
        partido="PXX",
        uf="SP",
        mandato="2023–2027",
        acessos=100,
    )
    db.add(p)
    db.commit()
    return p


def nova_promessa(
    db,
    parlamentar_id: str,
    autor_id: str,
    situacao: SituacaoModeracao = SituacaoModeracao.PENDENTE,
    status: StatusPromessa = StatusPromessa.SEM_ACAO,
    texto: str = "Construir 10 creches na periferia até 2026",
) -> Promessa:
    """Insere uma promessa direto no banco (sem passar pela verificação HTTP)."""
    promessa = Promessa(
        parlamentar_id=parlamentar_id,
        texto=texto,
        tema=Tema.EDUCACAO,
        fonte_url="https://exemplo.org/entrevista",
        fonte_descricao="Entrevista ao Portal Exemplo",
        data=date(2022, 8, 10),
        eleicao="2022",
        status=status,
        situacao=situacao,
        enviada_por_id=autor_id,
    )
    db.add(promessa)
    db.commit()
    db.refresh(promessa)
    return promessa


def dados_promessa(parlamentar_id: str) -> dict:
    return {
        "parlamentarId": parlamentar_id,
        "texto": "Construir 10 creches na periferia até 2026",
        "tema": "Educação",
        "fonteUrl": "https://exemplo.org/entrevista",
        "fonteDescricao": "Entrevista ao Portal Exemplo",
        "data": "2022-08-10",
        "eleicao": "2022",
    }
