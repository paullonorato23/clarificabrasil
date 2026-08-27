"""Fila de moderação colaborativa de promessas.

Regras de publicação (concepção do projeto):
- 3 validações da comunidade publicam a promessa automaticamente; ou
- um moderador aprova diretamente;
- um moderador pode rejeitar (motivo obrigatório): fonte inválida, paráfrase
  sem citação original, sátira/meme ou conteúdo envolvendo menores.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_usuario_atual, require_moderador
from app.enums import SituacaoModeracao, TipoValidacao
from app.models import Promessa, Usuario, Validacao
from app.schemas import PromessaPendenteOut, RejeicaoIn

router = APIRouter(prefix="/moderacao", tags=["moderação"])

VALIDACOES_PARA_PUBLICAR = 3


def _contagem(db: Session, promessa_id: str, tipo: TipoValidacao) -> int:
    return db.scalar(
        select(func.count())
        .select_from(Validacao)
        .where(Validacao.promessa_id == promessa_id, Validacao.tipo == tipo)
    ) or 0


def _fila_item(db: Session, p: Promessa) -> PromessaPendenteOut:
    return PromessaPendenteOut(
        id=p.id,
        texto=p.texto,
        tema=p.tema,
        fonte_url=p.fonte_url,
        fonte_descricao=p.fonte_descricao,
        data=p.data,
        eleicao=p.eleicao,
        status=p.status,
        acao_relacionada=p.acao_relacionada,
        parlamentar_id=p.parlamentar_id,
        validacoes=_contagem(db, p.id, TipoValidacao.VALIDACAO),
        questionamentos=_contagem(db, p.id, TipoValidacao.QUESTIONAMENTO),
        enviada_por=p.enviada_por.nome,
        fonte_verificada=p.fonte_verificada,
        fonte_status_http=p.fonte_status_http,
    )


def _pendente_ou_404(db: Session, promessa_id: str) -> Promessa:
    promessa = db.get(Promessa, promessa_id)
    if not promessa or promessa.situacao != SituacaoModeracao.PENDENTE:
        raise HTTPException(404, "Promessa não encontrada ou já moderada.")
    return promessa


def _impede_automoderacao(promessa: Promessa, moderador: Usuario) -> None:
    """Ninguém modera o próprio envio — nem moderadores. Regra de defesa
    contra manipulação: a decisão sobre uma promessa sempre passa por outra
    pessoa (comunidade ou outro moderador)."""
    if promessa.enviada_por_id == moderador.id:
        raise HTTPException(403, "Você não pode moderar o próprio envio.")


@router.get("/promessas", response_model=List[PromessaPendenteOut])
def fila(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    pendentes = db.scalars(
        select(Promessa)
        .where(Promessa.situacao == SituacaoModeracao.PENDENTE)
        .order_by(Promessa.criado_em)
    ).all()
    return [_fila_item(db, p) for p in pendentes]


def _registrar(
    promessa_id: str,
    tipo: TipoValidacao,
    db: Session,
    usuario: Usuario,
) -> PromessaPendenteOut:
    promessa = _pendente_ou_404(db, promessa_id)
    if promessa.enviada_por_id == usuario.id:
        raise HTTPException(403, "Você não pode validar a própria promessa.")

    ja_registrou = db.scalar(
        select(Validacao).where(
            Validacao.promessa_id == promessa_id,
            Validacao.usuario_id == usuario.id,
            Validacao.tipo == tipo,
        )
    )
    if ja_registrou:
        raise HTTPException(409, "Você já registrou esta ação nesta promessa.")

    db.add(Validacao(promessa_id=promessa_id, usuario_id=usuario.id, tipo=tipo))

    if tipo == TipoValidacao.VALIDACAO:
        total = _contagem(db, promessa_id, TipoValidacao.VALIDACAO) + 1
        if total >= VALIDACOES_PARA_PUBLICAR:
            promessa.situacao = SituacaoModeracao.PUBLICADA

    db.commit()
    db.refresh(promessa)
    return _fila_item(db, promessa)


@router.post("/promessas/{promessa_id}/validar", response_model=PromessaPendenteOut)
def validar(
    promessa_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    return _registrar(promessa_id, TipoValidacao.VALIDACAO, db, usuario)


@router.post("/promessas/{promessa_id}/questionar", response_model=PromessaPendenteOut)
def questionar(
    promessa_id: str,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    return _registrar(promessa_id, TipoValidacao.QUESTIONAMENTO, db, usuario)


@router.post("/promessas/{promessa_id}/aprovar", response_model=PromessaPendenteOut)
def aprovar(
    promessa_id: str,
    db: Session = Depends(get_db),
    moderador: Usuario = Depends(require_moderador),
):
    promessa = _pendente_ou_404(db, promessa_id)
    _impede_automoderacao(promessa, moderador)
    promessa.situacao = SituacaoModeracao.PUBLICADA
    db.commit()
    db.refresh(promessa)
    return _fila_item(db, promessa)


@router.post("/promessas/{promessa_id}/rejeitar", response_model=PromessaPendenteOut)
def rejeitar(
    promessa_id: str,
    dados: RejeicaoIn,
    db: Session = Depends(get_db),
    moderador: Usuario = Depends(require_moderador),
):
    promessa = _pendente_ou_404(db, promessa_id)
    _impede_automoderacao(promessa, moderador)
    promessa.situacao = SituacaoModeracao.REJEITADA
    promessa.motivo_rejeicao = dados.motivo
    db.commit()
    db.refresh(promessa)
    return _fila_item(db, promessa)
