"""Seed mínimo: cria o moderador inicial a partir de variáveis de ambiente.

Roda no startup apenas se ADMIN_EMAIL e ADMIN_SENHA estiverem definidas.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.enums import PapelUsuario
from app.models import Usuario
from app.security import hash_senha


def seed_moderador(db: Session) -> None:
    settings = get_settings()
    if not settings.admin_email or not settings.admin_senha:
        return
    existe = db.scalar(select(Usuario).where(Usuario.email == settings.admin_email))
    if existe:
        return
    db.add(
        Usuario(
            nome="Moderação",
            email=settings.admin_email,
            senha_hash=hash_senha(settings.admin_senha),
            papel=PapelUsuario.MODERADOR,
        )
    )
    db.commit()
