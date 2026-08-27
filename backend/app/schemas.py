"""Schemas Pydantic v2. O JSON trafega em camelCase para casar com os tipos
do frontend (`frontend/src/lib/types.ts`)."""

from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel

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


class SchemaBase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


# ---------------------------------------------------------------- auth

class RegistroIn(SchemaBase):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class LoginIn(SchemaBase):
    email: EmailStr
    senha: str


class TokenOut(SchemaBase):
    access_token: str
    token_type: str = "bearer"


class UsuarioOut(SchemaBase):
    id: str
    nome: str
    email: EmailStr
    papel: PapelUsuario


# ------------------------------------------------- entidades públicas

class PromessaOut(SchemaBase):
    """Shape `Promessa` do frontend."""

    id: str
    texto: str
    tema: Tema
    fonte_url: str
    fonte_descricao: str
    data: date
    eleicao: str
    status: StatusPromessa
    acao_relacionada: Optional[str] = None


class ProposicaoOut(SchemaBase):
    id: str
    tipo: TipoProposicao
    numero: str
    ementa: str
    tema: Optional[Tema] = None
    status: StatusProposicao
    data: date


class VotacaoOut(SchemaBase):
    id: str
    materia: str
    tema: Optional[Tema] = None
    data: date
    voto: VotoNominal
    coerente_com_discurso: Optional[bool] = None


class GastoOut(SchemaBase):
    categoria: str
    valor: float
    ano: int


class ParlamentarResumoOut(SchemaBase):
    id: str
    nome: str
    casa: Casa
    partido: str
    uf: str
    mandato: str
    acessos: int
    score: int


class ParlamentarDetalheOut(SchemaBase):
    """Shape `Parlamentar` do frontend, acrescido de score e resumo."""

    id: str
    nome: str
    casa: Casa
    partido: str
    uf: str
    mandato: str
    acessos: int
    promessas: List[PromessaOut]
    proposicoes: List[ProposicaoOut]
    votacoes: List[VotacaoOut]
    gastos: List[GastoOut]
    score: int
    resumo_promessas: Dict[str, int]


# ---------------------------------------------------- promessas/moderação

class PromessaIn(SchemaBase):
    parlamentar_id: str
    texto: str = Field(min_length=10)
    tema: Tema
    fonte_url: str = Field(max_length=1000)
    fonte_descricao: str = Field(min_length=3, max_length=300)
    data: date
    eleicao: str = Field(min_length=4, max_length=4)


class PromessaCriadaOut(PromessaOut):
    parlamentar_id: str
    situacao: SituacaoModeracao
    fonte_verificada: bool
    fonte_status_http: Optional[int] = None


class PromessaPendenteOut(PromessaOut):
    """Shape `PromessaPendente` do frontend (fila de moderação)."""

    parlamentar_id: str
    validacoes: int
    questionamentos: int
    enviada_por: str
    fonte_verificada: bool
    fonte_status_http: Optional[int] = None


class RejeicaoIn(SchemaBase):
    motivo: str = Field(min_length=3)
