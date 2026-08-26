"""Configuração da aplicação via variáveis de ambiente (ver .env.example)."""

from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Padrão local é SQLite para facilitar o desenvolvimento; produção usa PostgreSQL.
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = "troque-esta-chave-em-producao"
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:3000"
    fonte_http_timeout: float = 5.0
    admin_email: Optional[str] = None
    admin_senha: Optional[str] = None

    @property
    def cors_origins_list(self) -> List[str]:
        return [origem.strip() for origem in self.cors_origins.split(",") if origem.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
