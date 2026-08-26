"""Dependências FastAPI compartilhadas: sessão de banco e autenticação."""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums import PapelUsuario
from app.models import Usuario
from app.security import decodificar_token

_bearer = HTTPBearer(auto_error=True)
_bearer_opcional = HTTPBearer(auto_error=False)


def _buscar_usuario(cred: Optional[HTTPAuthorizationCredentials], db: Session) -> Optional[Usuario]:
    if cred is None:
        return None
    usuario_id = decodificar_token(cred.credentials)
    if not usuario_id:
        return None
    return db.get(Usuario, usuario_id)


def get_usuario_atual(
    cred: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    """Exige um token bearer válido."""
    usuario = _buscar_usuario(cred, db)
    if usuario is None:
        raise HTTPException(401, "Token ausente, inválido ou expirado.")
    return usuario


def get_usuario_opcional(
    cred: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_opcional),
    db: Session = Depends(get_db),
) -> Optional[Usuario]:
    """Autentica se houver token; segue anônimo caso contrário."""
    return _buscar_usuario(cred, db)


def require_moderador(usuario: Usuario = Depends(get_usuario_atual)) -> Usuario:
    if usuario.papel != PapelUsuario.MODERADOR:
        raise HTTPException(403, "Ação restrita a moderadores.")
    return usuario
