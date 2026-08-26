"""Hash de senhas (argon2 via pwdlib) e tokens JWT."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from pwdlib import PasswordHash

from app.config import get_settings

_ALGORITMO = "HS256"
_hasher = PasswordHash.recommended()


def hash_senha(senha: str) -> str:
    return _hasher.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return _hasher.verify(senha, senha_hash)
    except Exception:
        # Hash em formato desconhecido/corrompido não deve derrubar o login.
        return False


def criar_token_acesso(usuario_id: str) -> str:
    settings = get_settings()
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": usuario_id, "exp": expira}
    return jwt.encode(payload, settings.secret_key, algorithm=_ALGORITMO)


def decodificar_token(token: str) -> Optional[str]:
    """Retorna o id do usuário (sub) ou None se o token for inválido/expirado."""
    try:
        payload = jwt.decode(
            token, get_settings().secret_key, algorithms=[_ALGORITMO]
        )
        return payload.get("sub")
    except jwt.PyJWTError:
        return None
