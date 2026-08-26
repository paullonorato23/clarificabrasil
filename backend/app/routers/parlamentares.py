"""Consultas públicas: parlamentares, detalhe do perfil e ranking."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums import Casa, SituacaoModeracao
from app.models import Parlamentar, Promessa, Votacao
from app.schemas import (
    GastoOut,
    ParlamentarDetalheOut,
    ParlamentarResumoOut,
    PromessaOut,
    ProposicaoOut,
    VotacaoOut,
)
from app.score import calcular_score, resumo_promessas

router = APIRouter(tags=["parlamentares"])

LIMITE_RANKING = 10


def _promessas_publicadas(db: Session, parlamentar_id: str) -> List[Promessa]:
    return list(
        db.scalars(
            select(Promessa).where(
                Promessa.parlamentar_id == parlamentar_id,
                Promessa.situacao == SituacaoModeracao.PUBLICADA,
            )
        )
    )


def _votacoes(db: Session, parlamentar_id: str) -> List[Votacao]:
    return list(db.scalars(select(Votacao).where(Votacao.parlamentar_id == parlamentar_id)))


def _resumo(p: Parlamentar, score: int) -> ParlamentarResumoOut:
    return ParlamentarResumoOut(
        id=p.id,
        nome=p.nome,
        casa=p.casa,
        partido=p.partido,
        uf=p.uf,
        mandato=p.mandato,
        acessos=p.acessos,
        score=score,
    )


@router.get("/parlamentares", response_model=List[ParlamentarResumoOut])
def listar_parlamentares(
    busca: Optional[str] = None,
    casa: Optional[Casa] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    db: Session = Depends(get_db),
):
    stmt = select(Parlamentar)
    if busca:
        stmt = stmt.where(Parlamentar.nome.ilike(f"%{busca}%"))
    if casa:
        stmt = stmt.where(Parlamentar.casa == casa)
    if uf:
        stmt = stmt.where(Parlamentar.uf == uf.upper())
    if partido:
        stmt = stmt.where(Parlamentar.partido == partido.upper())
    parlamentares = db.scalars(stmt.order_by(Parlamentar.nome)).all()
    return [
        _resumo(p, calcular_score(_promessas_publicadas(db, p.id), _votacoes(db, p.id)))
        for p in parlamentares
    ]


@router.get("/parlamentares/{parlamentar_id}", response_model=ParlamentarDetalheOut)
def detalhe_parlamentar(parlamentar_id: str, db: Session = Depends(get_db)):
    p = db.get(Parlamentar, parlamentar_id)
    if not p:
        raise HTTPException(404, "Parlamentar não encontrado.")

    p.acessos += 1
    db.commit()

    # Apenas promessas publicadas são públicas; pendentes/rejeitadas ficam na moderação.
    promessas = _promessas_publicadas(db, p.id)
    votacoes = _votacoes(db, p.id)

    return ParlamentarDetalheOut(
        id=p.id,
        nome=p.nome,
        casa=p.casa,
        partido=p.partido,
        uf=p.uf,
        mandato=p.mandato,
        acessos=p.acessos,
        promessas=[PromessaOut.model_validate(pr) for pr in promessas],
        proposicoes=[ProposicaoOut.model_validate(pr) for pr in p.proposicoes],
        votacoes=[VotacaoOut.model_validate(v) for v in votacoes],
        gastos=[GastoOut.model_validate(g) for g in p.gastos],
        score=calcular_score(promessas, votacoes),
        resumo_promessas=resumo_promessas(promessas),
    )


@router.get("/ranking", response_model=List[ParlamentarResumoOut])
def ranking(
    por: str = Query("acessos", pattern="^(acessos|score)$"),
    db: Session = Depends(get_db),
):
    parlamentares = db.scalars(select(Parlamentar)).all()
    resumos = [
        _resumo(p, calcular_score(_promessas_publicadas(db, p.id), _votacoes(db, p.id)))
        for p in parlamentares
    ]
    chave = (lambda r: r.score) if por == "score" else (lambda r: r.acessos)
    resumos.sort(key=chave, reverse=True)
    return resumos[:LIMITE_RANKING]
