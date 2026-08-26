"""Modelos SQLAlchemy do domínio."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums import (
    Casa,
    PapelUsuario,
    SituacaoModeracao,
    StatusPromessa,
    StatusProposicao,
    Tema,
    TipoProposicao,
    TipoValidacao,
    VotoNominal,
)


def _uuid() -> str:
    return str(uuid.uuid4())


# native_enum=False grava o enum como VARCHAR com CHECK — funciona igual em
# SQLite (testes/dev) e PostgreSQL (produção), sem criar tipos nativos.
_Enum = lambda e: SAEnum(e, native_enum=False)  # noqa: E731


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    papel: Mapped[PapelUsuario] = mapped_column(_Enum(PapelUsuario), default=PapelUsuario.COMUM)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    promessas: Mapped[List["Promessa"]] = relationship(back_populates="enviada_por")


class Parlamentar(Base):
    __tablename__ = "parlamentares"

    # Slug usado na URL do frontend (ex.: "ana-beatriz-ramos").
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), index=True)
    casa: Mapped[Casa] = mapped_column(_Enum(Casa))
    partido: Mapped[str] = mapped_column(String(20))
    uf: Mapped[str] = mapped_column(String(2))
    mandato: Mapped[str] = mapped_column(String(60))
    acessos: Mapped[int] = mapped_column(Integer, default=0)

    promessas: Mapped[List["Promessa"]] = relationship(back_populates="parlamentar")
    proposicoes: Mapped[List["Proposicao"]] = relationship(back_populates="parlamentar")
    votacoes: Mapped[List["Votacao"]] = relationship(back_populates="parlamentar")
    gastos: Mapped[List["Gasto"]] = relationship(back_populates="parlamentar")


class Promessa(Base):
    __tablename__ = "promessas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    parlamentar_id: Mapped[str] = mapped_column(ForeignKey("parlamentares.id"), index=True)
    texto: Mapped[str] = mapped_column(Text)
    tema: Mapped[Tema] = mapped_column(_Enum(Tema))
    fonte_url: Mapped[str] = mapped_column(String(1000))
    fonte_descricao: Mapped[str] = mapped_column(String(300))
    data: Mapped[date] = mapped_column(Date)
    eleicao: Mapped[str] = mapped_column(String(4))
    status: Mapped[StatusPromessa] = mapped_column(
        _Enum(StatusPromessa), default=StatusPromessa.SEM_ACAO
    )
    acao_relacionada: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Moderação colaborativa: pendente → publicada (3 validações ou moderador) | rejeitada.
    situacao: Mapped[SituacaoModeracao] = mapped_column(
        _Enum(SituacaoModeracao), default=SituacaoModeracao.PENDENTE, index=True
    )
    motivo_rejeicao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Resultado da verificação automática do link da fonte (status HTTP).
    fonte_verificada: Mapped[bool] = mapped_column(default=False)
    fonte_status_http: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    enviada_por_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    parlamentar: Mapped[Parlamentar] = relationship(back_populates="promessas")
    enviada_por: Mapped[Usuario] = relationship(back_populates="promessas")
    validacoes: Mapped[List["Validacao"]] = relationship(
        back_populates="promessa", cascade="all, delete-orphan"
    )


class Validacao(Base):
    """Validação ou questionamento da comunidade sobre uma promessa pendente."""

    __tablename__ = "validacoes"
    __table_args__ = (
        UniqueConstraint("promessa_id", "usuario_id", "tipo", name="uq_validacao_unica"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    promessa_id: Mapped[str] = mapped_column(ForeignKey("promessas.id"), index=True)
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"))
    tipo: Mapped[TipoValidacao] = mapped_column(_Enum(TipoValidacao))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    promessa: Mapped[Promessa] = relationship(back_populates="validacoes")


class Proposicao(Base):
    __tablename__ = "proposicoes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    parlamentar_id: Mapped[str] = mapped_column(ForeignKey("parlamentares.id"), index=True)
    tipo: Mapped[TipoProposicao] = mapped_column(_Enum(TipoProposicao))
    numero: Mapped[str] = mapped_column(String(20))  # ex.: "1452/2023"
    ementa: Mapped[str] = mapped_column(Text)
    tema: Mapped[Tema] = mapped_column(_Enum(Tema))
    status: Mapped[StatusProposicao] = mapped_column(_Enum(StatusProposicao))
    data: Mapped[date] = mapped_column(Date)

    parlamentar: Mapped[Parlamentar] = relationship(back_populates="proposicoes")


class Votacao(Base):
    __tablename__ = "votacoes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    parlamentar_id: Mapped[str] = mapped_column(ForeignKey("parlamentares.id"), index=True)
    materia: Mapped[str] = mapped_column(String(300))
    tema: Mapped[Tema] = mapped_column(_Enum(Tema))
    data: Mapped[date] = mapped_column(Date)
    voto: Mapped[VotoNominal] = mapped_column(_Enum(VotoNominal))
    coerente_com_discurso: Mapped[bool] = mapped_column(default=True)

    parlamentar: Mapped[Parlamentar] = relationship(back_populates="votacoes")


class Gasto(Base):
    __tablename__ = "gastos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    parlamentar_id: Mapped[str] = mapped_column(ForeignKey("parlamentares.id"), index=True)
    categoria: Mapped[str] = mapped_column(String(120))
    valor: Mapped[float] = mapped_column(Float)
    ano: Mapped[int] = mapped_column(Integer)

    parlamentar: Mapped[Parlamentar] = relationship(back_populates="gastos")
