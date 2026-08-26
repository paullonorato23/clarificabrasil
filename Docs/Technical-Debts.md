# Débitos Técnicos

> Decisões conscientes que simplificaram a entrega, mas devem ser revistas
> antes da produção. Ordenadas por prioridade.

---

## Backend

### TD-01 — Sem migrações de banco (Alembic)
**O que é:** as tabelas são criadas com `Base.metadata.create_all` no startup
(`backend/main.py`).
**Risco:** evolução do schema em produção exige migração manual; `create_all`
não altera tabelas existentes.
**Resolver quando:** antes do primeiro deploy com dados reais.

### TD-02 — Verificação HTTP da fonte é síncrona
**O que é:** `POST /promessas` faz um GET externo no link da fonte durante o
request (`backend/app/fontes.py`), com timeout de 5s.
**Risco:** latência e disponibilidade do cadastro ficam reféns de sites de
terceiros; sob carga, vira gargalo.
**Resolver quando:** junto com o job de sincronização das APIs oficiais —
mover para fila/job assíncrono e revalidar periodicamente.

### TD-03 — JWT sem refresh token nem revogação
**O que é:** token único de acesso com expiração configurável
(default 60 min), sem lista de revogação.
**Risco:** um token vazado vale até expirar; logout não invalida o token.
**Resolver quando:** antes de abrir cadastro público em produção.

### TD-04 — Ranking e listagens calculam score em memória (N+1)
**O que é:** `GET /parlamentares` e `GET /ranking` consultam promessas e
votações por parlamentar e computam o score no Python
(`backend/app/routers/parlamentares.py`).
**Risco:** não escala para 594 parlamentares + histórico completo.
**Resolver quando:** na integração com as APIs oficiais — paginar, agregar
em SQL e/ou materializar o score com recálculo agendado.

### TD-05 — Contador de acessos sem proteção
**O que é:** `GET /parlamentares/{id}` incrementa `acessos` a cada chamada.
**Risco:** refresh/bots inflam o ranking "mais acessados".
**Resolver quando:** quando o ranking passar a ser exibido com dados reais.

### TD-06 — Sem rate limiting
**O que é:** cadastro de promessas, validações e login não têm limite de
requisições por usuário/IP.
**Risco:** abuso (spam de promessas, validações em massa, força bruta no login).
**Resolver quando:** antes do deploy público.

### TD-07 — Testes rodam em SQLite, produção em PostgreSQL
**O que é:** a suíte usa SQLite em memória; enums são gravados como VARCHAR
com CHECK (`native_enum=False`) justamente para equivalência.
**Risco:** diferenças sutis de comportamento (datas, collation, constraints).
**Resolver quando:** configurar CI — rodar a suíte também contra Postgres
(ex.: service container ou testcontainers).

### TD-08 — Sem envio de e-mail
**O que é:** não há confirmação de cadastro, recuperação de senha nem aviso
de moderação por e-mail.
**Resolver quando:** definir provedor (ex.: Resend, SES) na fase de deploy.

### TD-09 — Ambiente de desenvolvimento com Python 3.9
**O que é:** a suíte foi executada localmente em venv com Python 3.9.6
(sistema), embora o alvo documentado seja 3.11+. O código foi mantido
compatível com 3.9+, mas as versões resolvidas das dependências no 3.9 podem
ser mais antigas que as de produção.
**Resolver quando:** instalar Python 3.11+ na máquina (ver Docs/Doubts.md,
item 1) e fixar versões com lockfile.
