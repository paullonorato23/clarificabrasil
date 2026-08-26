# Status da Implementação

> Documento vivo de acompanhamento: o que está pronto, o que está parcial e o
> que falta — por frente de trabalho. Atualizado a cada sessão de implementação.
> O `PENDENCIAS.md` (raiz) é o plano original e não é editado.
>
> Última atualização: **25/08/2026** (backend inicial).

Legenda: ✅ pronto · 🟡 parcial · ⬜ pendente

---

## 1. Backend (`backend/` — FastAPI + SQLAlchemy + PostgreSQL/SQLite)

### Infraestrutura
- ✅ Estrutura do projeto, `requirements.txt`/`requirements-dev.txt`, `.env.example`, `.gitignore`, `README.md`
- ✅ Configuração via `.env` (DATABASE_URL, SECRET_KEY, CORS, timeouts)
- ✅ CORS, `/health`, criação automática de tabelas no startup
- ⬜ Migrações com Alembic (TD-01)
- ⬜ CI/CD (lint + pytest + build)

### Modelo de dados
- ✅ Usuários (papéis comum/moderador), parlamentares, promessas, validações, proposições, votações, gastos
- ⬜ Importação de dados reais (hoje o banco nasce vazio; frontend ainda usa mock)

### Autenticação e sessão
- ✅ Registro, login (JWT), `/auth/me`, hash argon2
- ✅ Seed de moderador via env
- ⬜ Refresh token / revogação de token (TD-03)
- ⬜ Confirmação de e-mail e recuperação de senha (TD-08 — falta disparar e-mail)
- ⬜ Rate limiting no login (TD-06)

### Promessas e moderação
- ✅ Cadastro autenticado com validação de URL e **verificação HTTP da fonte** (síncrona — TD-02 prevê mover para job)
- ✅ Fila de moderação com contagens e autor
- ✅ Publicação após 3 validações da comunidade ou aprovação de moderador
- ✅ Rejeição por moderador com motivo obrigatório
- ✅ **Moderador não modera o próprio envio** (regra anti-manipulação, 25/08 tarde)
- ⬜ **Visibilidade pública total da moderação** (pendentes e rejeitadas + motivo, sem login — decisão 8 em Docs/Doubts.md; muda comportamento atual da API e pede UX por abas)
- ⬜ **Snapshot da fonte via Wayback Machine** + campo de citação literal (decisão 10)
- ⬜ Revalidação periódica de links de fontes já publicadas
- ⬜ Notificação ao autor quando a promessa é publicada/rejeitada (depende de e-mail — Resend escolhido como provedor)

### Anti-abuso (PRIORIDADE 0 — decidido em 25/08)
- ⬜ Verificação de e-mail no registro (conta só ativa após confirmar)
- ⬜ Captcha (Cloudflare Turnstile) em registro, login e cadastro de promessa
- ⬜ Rate limiting por IP/usuário (registro, login, promessas, validações)
- ⬜ **Reputação progressiva** com limites por conta nova → contas maduras (decisão 11; regra deve ser pública no site)
- ⬜ Backoffice de moderação: fila por risco, banimento de contas, auditoria

### Parlamentares e ranking
- ✅ Listagem com filtros, detalhe completo, ranking por acessos/score
- ✅ Detalhe expõe apenas promessas publicadas
- 🟡 Ranking "mais acessados": funciona, mas o contador é inflável (TD-05)
- 🟡 Score calculado em memória por request (TD-04 — materializar quando houver dados reais)

### Score de Coerência
- ✅ v0.1 portada do frontend e testada
- ⬜ Evolução versionada da metodologia (v0.2+)

### Testes
- ✅ 45 testes passando (`pytest`), cobrindo score, auth, parlamentares, promessas e moderação
- 🟡 Rodam em SQLite; falta pipeline contra PostgreSQL (TD-07)

## 2. Frontend (`frontend/` — Next.js, sem alterações nesta sessão)
- ✅ Páginas do MVP navegável com dados mock (ver PENDENCIAS.md seção 1)
- ⬜ Consumir a API real no lugar de `data/mock.ts`
- ⬜ Telas de autenticação (login/registro) — a API já existe, a UI não
- ⬜ Ligar `/promessas/nova` ao `POST /promessas` (hoje o envio é simulado)
- ⬜ Ligar `/moderacao` à fila real (`GET/POST /moderacao/...`)
- ⬜ 404/`loading.tsx`, `frontend/README.md`, `frontend/.env.example`, testes do frontend

## 3. Integração com fontes oficiais
- ⬜ API Dados Abertos da Câmara (deputados, proposições, votações, despesas)
- ⬜ API do Senado Federal
- ⬜ Base dos Dados (avaliação)
- ⬜ Job de sincronização periódica + cache

## 4. Inteligência (fase posterior)
- ⬜ Categorização automática de proposições por tema
- ⬜ Cruzamento automático promessa ↔ ação e alertas de contradição
- ⬜ Frequência em plenário, linha do tempo, comparação por estado

## 5. Infra e identidade
- ⬜ Deploy (Vercel + Railway/Render)
- ⬜ Logo/favicon reais, revisão de acessibilidade
- 🟡 `AGENTS.md` da raiz atualizado quanto ao backend; revisar novamente após próximas fases

---

### Próxima sessão sugerida
1. Resolver ambiente Python 3.11+ (Docs/Doubts.md item 1) e fixar lockfile
2. Integração com a API da Câmara (maior valor: dados reais)
3. Frontend: telas de login/registro e consumo da API
