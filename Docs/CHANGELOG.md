# Changelog

> Registro das implementações do projeto. O `PENDENCIAS.md` (raiz) descreve o
> plano original e **não é editado**; o acompanhamento vivo fica em
> `Docs/Status.md`.

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/), datas em AAAA-MM-DD.

---

## [Não lançado]

### 2026-08-27 — Integração com a API da Câmara (issue #8)

- **Cliente HTTP** (`backend/app/integracoes/camara.py`): paginação automática,
  endpoints de deputados, legislaturas, proposições, votações, votos nominais
  e despesas de gabinete; timeout e URL configuráveis por env
  (`CAMARA_API_URL`, `CAMARA_HTTP_TIMEOUT`); suporta `MockTransport` nos testes.
- **Sincronização idempotente** (`backend/app/integracoes/sincronizacao.py`):
  deputados → `Parlamentar` (slug único, mandato da legislatura atual),
  proposições (PL/PEC/REQ), votos nominais recentes e despesas agregadas por
  categoria/ano. CLI: `python -m app.integracoes.sincronizacao --etapa ...`.
- **Modelo**: novos campos `id_camara` (Parlamentar, Proposicao, Votacao) para
  upsert sem duplicar; `tema` de Proposicao/Votacao e `coerente_com_discurso`
  de Votacao passaram a ser opcionais (decisões 13–15 em `Docs/Doubts.md`).
- **Score v0.1 — esclarecimento**: votos sem avaliação editorial (`None`) são
  ignorados no cálculo; se nenhum voto foi avaliado, as promessas assumem
  peso total.
- **Testes**: 8 novos testes com HTTP 100% mockado (55 no total, todos
  passando) + smoke test manual contra a API real da Câmara.
- A agenda periódica desta sincronização é a issue #23.

### 2026-08-25 — Backend: implementação inicial (do zero)

**Infraestrutura do backend (`backend/`)**
- Estrutura FastAPI criada do zero: entrypoint `uvicorn main:app`, configuração
  via `.env` (pydantic-settings), `requirements.txt`/`requirements-dev.txt`,
  `.env.example`, `.gitignore` e `README.md` próprio.
- SQLAlchemy 2.0 com modelos: `Usuario`, `Parlamentar`, `Promessa`,
  `Validacao`, `Proposicao`, `Votacao`, `Gasto`. Enums de domínio com os
  mesmos valores dos tipos do frontend; enums gravados como VARCHAR + CHECK
  para equivalência SQLite/PostgreSQL.
- JSON da API serializado em camelCase (Pydantic v2 com `alias_generator`),
  casando com `frontend/src/lib/types.ts`.
- CORS configurável, `GET /health`, criação automática de tabelas no startup.

**Autenticação e papéis**
- `POST /auth/registro` (senha mín. 8, e-mail único, hash argon2 via pwdlib),
  `POST /auth/login` (JWT HS256), `GET /auth/me`.
- Papéis `comum` e `moderador`; dependência `require_moderador`.
- Seed opcional de moderador via `ADMIN_EMAIL`/`ADMIN_SENHA`.

**Parlamentares (público)**
- `GET /parlamentares` com filtros `busca`, `casa`, `uf`, `partido` e score
  calculado apenas com promessas publicadas.
- `GET /parlamentares/{id}` com promessas publicadas, proposições, votações,
  gastos, score e resumo de promessas; incrementa `acessos`.
- `GET /ranking?por=acessos|score` (top 10).

**Promessas e moderação colaborativa**
- `POST /promessas` autenticado, com validação de formato da URL da fonte e
  **verificação automática do link** (status HTTP via httpx, timeout
  configurável); falha na verificação não bloqueia o cadastro — marca
  `fonte_verificada=false`.
- `GET /promessas/{id}`: pendentes/rejeitadas visíveis só a autor e moderadores.
- Fila de moderação (`GET /moderacao/promessas`) com contagens de validações
  e questionamentos e nome do autor.
- Regras: publicação automática após **3 validações** da comunidade ou
  aprovação de moderador; rejeição por moderador com motivo obrigatório;
  autor não valida a própria promessa; uma ação por usuário por tipo.

**Score de Coerência v0.1**
- Portado fielmente do frontend para `backend/app/score.py` (70% promessas +
  30% votações; peso total da fonte presente quando a outra está vazia), com
  `resumo_promessas`, `percentual_entrega` e `percentual_votos_coerentes`.

**Testes**
- Suíte pytest com **45 testes passando** (SQLite em memória, verificação HTTP
  mockada): score (fórmula e casos de borda), auth, listagem/detalhe/ranking
  de parlamentares, cadastro de promessas e todas as regras de moderação.

**Documentação viva (`Docs/`)**
- `Docs/Doubts.md`, `Docs/Technical-Debts.md` (TD-01 a TD-09),
  `Docs/CHANGELOG.md` (este arquivo) e `Docs/Status.md`.

**Não incluído nesta sessão (próximas fases, ver Docs/Status.md):**
integração com APIs da Câmara/Senado, migração do frontend para consumir a
API, Alembic, e-mails, CI/CD e deploy.
