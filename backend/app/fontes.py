"""Verificação automática do link da fonte de uma promessa (status HTTP).

Prevista na concepção do projeto: toda promessa exige fonte verificável.
O resultado é gravado na promessa (`fonte_verificada`, `fonte_status_http`)
e considerado pela moderação.
"""

from __future__ import annotations

from typing import Optional, Tuple
from urllib.parse import urlparse

import httpx


def url_valida(url: str) -> bool:
    """Formato mínimo exigido: http(s) com host."""
    try:
        partes = urlparse(url)
    except ValueError:
        return False
    return partes.scheme in ("http", "https") and bool(partes.netloc)


def verificar_fonte(url: str, timeout: float = 5.0) -> Tuple[bool, Optional[int]]:
    """Faz um GET no link da fonte.

    Retorna (ok, status_http): ok=True quando o servidor responde com status
    < 400; status_http é None quando não houve resposta (timeout, DNS etc.).
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=timeout) as cliente:
            resposta = cliente.get(url)
        return resposta.status_code < 400, resposta.status_code
    except httpx.HTTPError:
        return False, None
