# Avaliação — Base dos Dados como fonte complementar

> Resolução da issue #27. Avaliação feita em 26/08/2026.
> Fontes: [blog da BD — analisando os dados da Câmara](https://basedosdados.org/blog/de-olho-na-camara-analisando-dados-abertos-da-camara-dos-deputados-com-a-bd),
> [repositório dbt da BD (queries-basedosdados)](https://github.com/basedosdados/queries-basedosdados/tree/main/models/br_camara_dados_abertos),
> [página do conjunto na BD](https://basedosdados.org/dataset/br-camara-dados-abertos).

## Pergunta

A Base dos Dados (BD) deve ser usada como fonte de dados consolidados/históricos,
complementando as APIs oficiais da Câmara (#8) e do Senado (#9)?

## O que a BD oferece

A BD mantém o conjunto público `basedosdados.br_camara_dados_abertos` no
BigQuery, capturado do portal de Dados Abertos da Câmara, tratado com dbt
(com testes de qualidade) e **atualizado diariamente desde 2023**. Acesso via
SQL (BigQuery), Python, R e download de CSV.

Tabelas relevantes para o nosso modelo de dados:

| Tabela BD | Nosso modelo | Cobertura histórica |
|---|---|---|
| `deputado` | `Parlamentar` | todas as legislaturas |
| `legislatura` | apoio (mandato) | desde 1826 |
| `proposicao_microdados` | `Proposicao` | desde 1899 |
| `proposicao_autor` | vínculo proposição ↔ autor | desde 1934 |
| `proposicao_tema` | tema da proposição | desde 1946 |
| `votacao` / `votacao_objeto` / `votacao_proposicao` | `Votacao` (contexto) | desde 1934 |
| `votacao_parlamentar` | voto nominal por deputado | — |
| `despesa` | `Gasto` | desde 1959 |
| `evento_presenca_deputado` | frequência em plenário (#30) | desde 1900 |
| `orgao_deputado` | participação em comissões | — |

**Senado: a BD não tem conjunto tratado do Senado** (verificado no repositório
dbt oficial — só existe `br_camara_dados_abertos`). O Senado continua
dependendo da API própria (issue #9).

## Pontos fortes

- **Profundidade histórica** que a API da Câmara não entrega com praticidade
  (despesas desde 1959, votações desde 1934) — viabiliza comparar mandatos
  passados e pré-carregar o banco (backfill).
- Dados **tratados e com testes de qualidade** (manual de estilo da BD + dbt).
- `evento_presenca_deputado` cobre a issue #30 (frequência em plenário) sem
  scraping adicional.
- Grátis para consultas SQL dentro do free tier do BigQuery (1 TB/mês de
  processamento) — mais que suficiente para um job diário filtrado.

## Limitações

- Exige **conta GCP/BigQuery** e credencial de serviço — uma dependência a mais
  na infraestrutura.
- O plano grátis da BD prioriza dados de baixa frequência; o acesso às
  versões mais frescas pode exigir **BD Pro** (a partir de R$ 47/mês). Para
  backfill histórico isso não importa; para dados do dia, importa.
- É uma **fonte secundária**: se a BD atrasar ou quebrar o pipeline, nossos
  dados atrasam junto. A fonte primária deve continuar sendo a API oficial.

## Decisão

**Usar a BD como fonte complementar, não primária.** Concretamente:

1. **API oficial da Câmara (#8) segue como fonte primária** para dados
   correntes (frescor garantido, sem intermediário).
2. **BD para backfill histórico**: carga inicial de deputados, proposições,
   votações e despesas de legislaturas anteriores (credencial BigQuery via env).
3. **BD para frequência em plenário** (#30), que a tabela
   `evento_presenca_deputado` já resolve.
4. **Validação cruzada pontual**: comparar amostras BD × API oficial no job de
   sincronização (#23) para detectar divergências.
5. **Senado**: fora do escopo da BD; segue pela API do Senado (#9).

A implementação do backfill entra no escopo das issues #8 (integração Câmara)
e #23 (job de sincronização); não há pipeline novo específico da BD a criar
agora. Se a necessidade de dados diários via BD crescer, reavaliar o BD Pro.
