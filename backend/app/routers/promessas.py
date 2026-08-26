"""Cadastro colaborativo de promessas e consulta individual."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import fontes
from app.config import get_settings
from app.database import get_db
from app.deps import get_usuario_atual, get_usuario_opcional
from app.enums import PapelUsuario, SituacaoModeracao, StatusPromessa
from app.models import Parlamentar, Promessa, Usuario
from app.schemas import PromessaCriadaOut, PromessaIn

router = APIRouter(prefix="/promessas", tags=["promessas"])


@router.post("", response_model=PromessaCriadaOut, status_code=201)
def criar_promessa(
    dados: PromessaIn,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    if not db.get(Parlamentar, dados.parlamentar_id):
        raise HTTPException(404, "Parlamentar não encontrado.")
    if not fontes.url_valida(dados.fonte_url):
        raise HTTPException(422, "URL da fonte inválida: use um link http(s) completo.")

    # Verificação automática do link (status HTTP). Se falhar, a promessa é
    # criada mesmo assim, marcada como não verificada — a moderação decide.
    verificada, status_http = fontes.verificar_fonte(
        dados.fonte_url, timeout=get_settings().fonte_http_timeout
    )

    promessa = Promessa(
        parlamentar_id=dados.parlamentar_id,
        texto=dados.texto,
        tema=dados.tema,
        fonte_url=dados.fonte_url,
        fonte_descricao=dados.fonte_descricao,
        data=dados.data,
        eleicao=dados.eleicao,
        status=StatusPromessa.SEM_ACAO,
        situacao=SituacaoModeracao.PENDENTE,
        fonte_verificada=verificada,
        fonte_status_http=status_http,
        enviada_por_id=usuario.id,
    )
    db.add(promessa)
    db.commit()
    db.refresh(promessa)
    return promessa


@router.get("/{promessa_id}", response_model=PromessaCriadaOut)
def obter_promessa(
    promessa_id: str,
    db: Session = Depends(get_db),
    usuario: Optional[Usuario] = Depends(get_usuario_opcional),
):
    promessa = db.get(Promessa, promessa_id)
    if not promessa:
        raise HTTPException(404, "Promessa não encontrada.")

    # Promessas ainda em moderação (ou rejeitadas) só são visíveis ao autor e a moderadores.
    if promessa.situacao != SituacaoModeracao.PUBLICADA:
        autorizado = usuario and (
            usuario.id == promessa.enviada_por_id
            or usuario.papel == PapelUsuario.MODERADOR
        )
        if not autorizado:
            raise HTTPException(403, "Promessa ainda não publicada.")

    return promessa
