"""Cliente HTTP para a API de Dados Abertos da Câmara dos Deputados.

Documentação oficial: https://dadosabertos.camara.leg.br/swagger/api.html

Encapsula paginação e os endpoints usados pela sincronização (issue #8).
Aceita `transport` do httpx para testes sem rede (httpx.MockTransport).
"""

from __future__ import annotations

from typing import Dict, Iterator, List, Optional

import httpx

from app.config import get_settings

ITENS_POR_PAGINA = 100


class CamaraClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        transport: Optional[httpx.BaseTransport] = None,
    ):
        settings = get_settings()
        self._cliente = httpx.Client(
            base_url=base_url or settings.camara_api_url,
            timeout=timeout or settings.camara_http_timeout,
            headers={"Accept": "application/json"},
            transport=transport,
        )

    def close(self) -> None:
        self._cliente.close()

    def __enter__(self) -> "CamaraClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def _get_json(self, caminho: str, params: Optional[Dict] = None) -> Dict:
        resposta = self._cliente.get(caminho, params=params)
        resposta.raise_for_status()
        return resposta.json()

    def _paginar(self, caminho: str, params: Optional[Dict] = None) -> Iterator[Dict]:
        """Percorre todas as páginas de um endpoint de listagem."""
        pagina = 1
        while True:
            corpo = self._get_json(
                caminho,
                params={**(params or {}), "pagina": pagina, "itens": ITENS_POR_PAGINA},
            )
            yield from corpo.get("dados", [])
            links = {link["rel"] for link in corpo.get("links", [])}
            if "next" not in links:
                break
            pagina += 1

    # ---------------------------------------------------------- endpoints

    def listar_deputados(self) -> List[Dict]:
        """Deputados em exercício: id, nome, siglaPartido, siglaUf, urlFoto..."""
        return list(self._paginar("/deputados", {"ordem": "ASC", "ordenarPor": "nome"}))

    def legislatura_atual(self) -> Dict:
        """Legislatura mais recente (dataInicio/dataFim), para compor o mandato."""
        corpo = self._get_json(
            "/legislaturas", {"ordem": "DESC", "ordenarPor": "id", "itens": 1}
        )
        return corpo["dados"][0]

    def listar_proposicoes_autor(self, id_deputado: int) -> List[Dict]:
        """Proposições de autoria do deputado: id, siglaTipo, numero, ano, ementa..."""
        return list(
            self._paginar(
                "/proposicoes",
                {"idDeputadoAutor": id_deputado, "ordem": "DESC", "ordenarPor": "id"},
            )
        )

    def detalhe_proposicao(self, id_proposicao: int) -> Dict:
        return self._get_json(f"/proposicoes/{id_proposicao}")["dados"]

    def listar_votacoes(self, data_inicio: str, data_fim: str) -> List[Dict]:
        """Votações nominais no período (datas AAAA-MM-DD)."""
        return list(
            self._paginar(
                "/votacoes",
                {
                    "dataInicio": data_inicio,
                    "dataFim": data_fim,
                    "ordem": "DESC",
                    "ordenarPor": "dataHoraRegistro",
                },
            )
        )

    def listar_votos(self, id_votacao: str) -> List[Dict]:
        """Votos nominais de uma votação: tipoVoto + deputado (id, nome...)."""
        return list(self._paginar(f"/votacoes/{id_votacao}/votos", {"itens": 500}))

    def listar_despesas(self, id_deputado: int, ano: int) -> List[Dict]:
        """Despesas de gabinete (CEAP) do deputado no ano."""
        return list(
            self._paginar(
                f"/deputados/{id_deputado}/despesas",
                {"ano": ano, "ordem": "ASC", "ordenarPor": "mes"},
            )
        )
