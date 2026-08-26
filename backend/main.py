"""Entrypoint da API — rode com `uvicorn main:app --reload`."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models  # noqa: F401 — registra as tabelas no metadata
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import auth, moderacao, parlamentares, promessas
from app.seed import seed_moderador

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Criação automática das tabelas: suficiente para o MVP.
    # Migrações com Alembic ficam como débito técnico (ver Docs/Technical-Debts.md).
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_moderador(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Política Transparente API",
    description="API da plataforma de monitoramento de parlamentares: promessas, proposições, votações, gastos e Score de Coerência.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(parlamentares.router)
app.include_router(promessas.router)
app.include_router(moderacao.router)


@app.get("/health", tags=["saúde"])
def health():
    return {"status": "ok"}
