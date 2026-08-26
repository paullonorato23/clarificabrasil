"""Registro, login e identidade do usuário autenticado."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_usuario_atual
from app.enums import PapelUsuario
from app.models import Usuario
from app.schemas import LoginIn, RegistroIn, TokenOut, UsuarioOut
from app.security import criar_token_acesso, hash_senha, verificar_senha

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registro", response_model=UsuarioOut, status_code=201)
def registrar(dados: RegistroIn, db: Session = Depends(get_db)):
    existente = db.scalar(select(Usuario).where(Usuario.email == dados.email))
    if existente:
        raise HTTPException(409, "E-mail já cadastrado.")
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
        papel=PapelUsuario.COMUM,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=TokenOut)
def login(dados: LoginIn, db: Session = Depends(get_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.email == dados.email))
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(401, "Credenciais inválidas.")
    return TokenOut(access_token=criar_token_acesso(usuario.id))


@router.get("/me", response_model=UsuarioOut)
def me(usuario: Usuario = Depends(get_usuario_atual)):
    return usuario
