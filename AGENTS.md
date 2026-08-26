# AGENTS.md — Política Transparente

> Guia para agentes de codificação (AI coding agents) que trabalham neste repositório.
> Este arquivo pressupõe que o leitor não conhece o projeto.

## 1. Visão geral do projeto

**Política Transparente** é uma plataforma colaborativa e sem fins lucrativos para monitorar a atuação de deputados federais e senadores brasileiros, cruzando **promessas de campanha** com **proposições, votações e gastos** — tudo com dados oficiais e código aberto.

Funcionalidades planejadas (ver `README.md`):

- Cadastro colaborativo de promessas de campanha, com fonte verificável e moderação
- Acompanhamento de proposições (PLs, PECs, requerimentos) via APIs oficiais
- Registro de votações nomeadas com análise de coerência
- Transparência de gastos de gabinete
- **Score de Coerência** (metodologia pública, auditável e versionada neste repositório)
- Comparador lado a lado de parlamentares

### Fontes de dados

- [API Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/)
- [API do Senado Federal](https://www12.senado.leg.br/dados-abertos)
- [Base dos Dados](https://basedosdados.org/)

### Princípios do projeto

- **Apartidário**: evite discussões político-partidárias nos canais técnicos; o foco é transparência de dados.
- **Sem fins lucrativos e independente**: não aceita financiamento de partidos ou entidades com interesses legislativos.
- Licença **MIT** (ver `LICENSE`, copyright Paullo Norato).

## 2. Estado atual do repositório — LEIA ANTES DE AGIR

O repositório já tem código-fonte em duas frentes:

```
.
├── backend/    # API FastAPI + SQLAlchemy (modelos, auth JWT, moderação, score, testes pytest)
├── frontend/   # Next.js 16 + React 19 + Tailwind 4 (MVP navegável com dados mock)
├── Docs/       # Documentação viva: Doubts.md, Technical-Debts.md, CHANGELOG.md, Status.md
├── PENDENCIAS.md  # Plano original (não editar; o acompanhamento vivo é Docs/Status.md)
├── README.md   # Visão geral, stack, instruções de setup
├── CONTRIBUTING.md / LICENSE / DESIGN_SYSTEM.md
└── AGENTS.md   # Este arquivo
```

Consequências práticas para agentes:

- **Não invente** módulos, testes ou convenções "existentes" — confira sempre se o arquivo/diretório realmente existe antes de afirmar que algo é padrão do projeto.
- O frontend ainda consome `frontend/src/data/mock.ts`; a migração para a API real é pendência (ver `Docs/Status.md`).
- Documentação viva do projeto fica em `Docs/`: dúvidas em `Doubts.md`, débitos em `Technical-Debts.md`, histórico em `CHANGELOG.md`, acompanhamento em `Status.md`. Atualize-os ao implementar.
- O frontend tem seu próprio guia em `frontend/AGENTS.md`.

## 3. Stack e arquitetura planejadas

Conforme o `README.md`:

| Camada | Tecnologia planejada |
|---|---|
| Frontend | React / Next.js / TailwindCSS |
| Backend | Python / FastAPI |
| Banco de dados | PostgreSQL 15+ |
| Dados | APIs oficiais da Câmara e do Senado + Base dos Dados |
| Deploy | A definir — Vercel (frontend) + Railway/Render (backend) sugeridos |

Estrutura de diretórios esperada (monorepo simples):

```
backend/    # FastAPI (Python 3.11+), entrypoint uvicorn main:app
frontend/   # Next.js (Node.js 18+), npm run dev na porta 3000
```

Ambos usam arquivos `.env.example` como modelo de configuração (`backend/.env`, `frontend/.env.local`).

## 4. Comandos de build, execução e teste

### Backend (`backend/`)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env      # opcional em dev: sem DATABASE_URL usa SQLite
uvicorn main:app --reload
```

Testes do backend: `pytest` (SQLite em memória, sem rede nem PostgreSQL).

### Frontend (`frontend/`)

```bash
cd frontend
npm install
npm run dev               # http://localhost:3000
```

Testes do frontend: `npm test` (**ainda não configurado** — sem framework de testes instalado).

### Pré-requisitos de ambiente

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

## 5. Convenções de desenvolvimento

Extraídas de `CONTRIBUTING.md` — siga-as ao contribuir:

### Idioma

- **Commits claros e descritivos em português.**
- Documentação e comunicação do projeto são em **português brasileiro**.

### Branches

Formato: `tipo/descrição-curta`. Exemplos:

- `feature/score-coerencia-algoritmo`
- `fix/api-camara-timeout`
- `docs/readme-instalacao`

### Commits

Formato sugerido:

```
[tipo] descrição curta

Descrição mais detalhada se necessário.

Refs: #123
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

### Pull Requests — checklist

- [ ] Código compila/roda sem erros
- [ ] Testes passam (`npm test` / `pytest`)
- [ ] Não há `console.log` ou debug esquecido
- [ ] Documentação atualizada
- [ ] Commits organizados e descritivos
- [ ] Não introduz dependências desnecessárias

### Estilo de código

- "Siga o estilo de código existente" (CONTRIBUTING.md): PEP 8 no backend (identificadores e docstrings em pt-BR), convenções do Next.js/React no frontend. Mantenha consistência daí em diante.

## 6. Estratégia de testes

- Backend: `pytest` em `backend/tests/` (45 testes; SQLite em memória, sem rede).
- Frontend: `npm test` (ainda não configurado).
- "Adicione testes quando aplicável" (CONTRIBUTING.md) — ao implementar código novo, inclua testes correspondentes.

## 7. Considerações de segurança e dados

- **Credenciais**: configuração via `.env` / `.env.local`, sempre a partir de `.env.example`. Nunca commitar arquivos `.env` com credenciais reais (ex.: PostgreSQL).
- **Promessas de campanha** passam por moderação e exigem fonte verificável; **não** são aceitos: promessas sem fonte, paráfrases sem citação original, conteúdo de humor/sátira/meme e **informações de menores de idade**.
- O sistema verifica o link da fonte (status HTTP); promessas são publicadas após 3 validações da comunidade ou aprovação de moderador.
- A metodologia do **Score de Coerência** deve permanecer pública, auditável e versionada neste repositório — mudanças no algoritmo devem ser documentadas.
