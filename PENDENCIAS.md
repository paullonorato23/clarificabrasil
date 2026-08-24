# Pendências — Política Transparente

> Levantamento do que já existe no repositório vs. o que foi planejado na concepção do projeto.
> Atualizado em 24/08/2026. Documento de acompanhamento da implementação.

---

## 1. O que já está implementado

### Documentação
- `README.md` — visão geral, stack planejada, instruções de setup
- `CONTRIBUTING.md` — convenções de branches, commits e PRs
- `AGENTS.md` (raiz) — guia para agentes (**parcialmente desatualizado**: ainda descreve o repositório como pré-implementação)
- `DESIGN_SYSTEM.md` — paleta, tipografia, espaçamento e tokens CSS (tokens e base visual aplicados ao frontend)
- `LICENSE` — MIT

### Frontend (`frontend/` — Next.js 16 + React 19 + Tailwind 4 + TypeScript)

**Páginas existentes:**
- `/` (home) — hero com busca, estatísticas gerais, ranking por score, "mais acessados", CTAs
- `/parlamentares` — lista com busca e filtros (casa, UF, partido)
- `/parlamentares/[id]` — perfil dinâmico com score, resumo e abas de promessas, proposições, votações e gastos
- `/comparar` — comparação lado a lado de dois parlamentares
- `/promessas/nova` — cadastro de promessa com envio simulado
- `/moderacao` — fila de promessas pendentes com validação simulada
- `/metodologia` — explicação pública do Score de Coerência v0.1
- `/sobre` — apresentação institucional do projeto

**Componentes utilizados nas telas:**
- `PerfilTabs.tsx` — navegação por abas do perfil
- `TabelaProposicoes.tsx` — tabela de PLs/PECs/REQs com filtros
- `GastosChart.tsx` — gráfico de barras de gastos por categoria
- `StatusPromessaBadge.tsx` — badge de status de promessa
- `ComparadorClient.tsx` — comparação lado a lado (pronto e funcional)
- `FormularioPromessa.tsx` — cadastro de promessa (envio apenas simulado)
- `BotoesValidacao.tsx` — validar/questionar na moderação (simulado)

**Bibliotecas e dados:**
- `lib/types.ts` — modelos: `Parlamentar`, `Promessa`, `PromessaPendente`, `Proposicao`, `Votacao`, `GastoCategoria`
- `lib/score.ts` — Score de Coerência **v0.1** (70% promessas + 30% votações, com faixas de cor)
- `lib/format.ts` — formatação de moeda, data e rótulos
- `data/mock.ts` — 6 parlamentares **fictícios** + 3 promessas pendentes (moderação)

### O que ainda NÃO existe
- `backend/` — nada foi criado (sem FastAPI, sem PostgreSQL, sem `.env.example`)
- Nenhuma integração com APIs oficiais (Câmara, Senado, Base dos Dados)
- Nenhum teste (frontend ou backend)
- Nenhuma CI/CD ou configuração de deploy

---

## 2. Pendências — Frontend (curto prazo, sem backend)

As rotas principais do MVP navegável foram implementadas com dados mock e sem backend:

- [x] **`/parlamentares/[id]`** — página de perfil do parlamentar com `PerfilTabs` e 4 abas:
  - Promessas vs. Ações (com `StatusPromessaBadge` e link para ação relacionada)
  - Proposições (com `TabelaProposicoes`)
  - Votações (voto nominal + indicador de coerência)
  - Gastos (com `GastosChart`, total e comparação com a média da bancada — `mediaGastoBancada()` já existe no mock)
- [x] **`/comparar`** — página que renderiza o `ComparadorClient`
- [x] **`/promessas/nova`** — página que renderiza o `FormularioPromessa` (envio simulado)
- [x] **`/moderacao`** — fila de promessas pendentes com `BotoesValidacao` (ações simuladas)
- [x] **`/metodologia`** — página pública explicando o Score de Coerência v0.1
- [x] **`/sobre`** — página institucional
- [ ] Página 404 (`not-found.tsx`) e estados de carregamento (`loading.tsx`)
- [ ] `frontend/README.md` — substituir o boilerplate do `create-next-app` por documentação real do projeto
- [ ] `frontend/.env.example` — modelo de configuração (mencionado no README raiz, não existe)
- [ ] Testes do frontend (`npm test` não está configurado — sem framework de testes instalado)

---

## 3. Pendências — Backend (do zero)

Conforme stack planejada (Python 3.11+ / FastAPI / PostgreSQL 15+):

- [ ] Criar estrutura `backend/` com `requirements.txt`, `.env.example` e entrypoint `uvicorn main:app`
- [ ] Modelo de dados (PostgreSQL): parlamentares, promessas, proposições, votações, gastos, validações de comunidade, usuários/moderadores
- [ ] Endpoints REST que o frontend consumirá (substituindo `data/mock.ts`)
- [ ] Autenticação e papéis (usuário comum vs. moderador)
- [ ] Regras de moderação no servidor: publicação após **3 validações da comunidade** ou aprovação de moderador; rejeição de promessas sem fonte, paráfrases, sátira e conteúdo envolvendo menores
- [ ] **Verificação automática do link da fonte** (checagem de status HTTP), prevista na concepção
- [ ] Testes com `pytest`

---

## 4. Pendências — Integração com fontes oficiais

- [ ] **API Dados Abertos da Câmara** — importar deputados, proposições, votações nominais e despesas de gabinete (`/deputados`, `/proposicoes`, `/votacoes`, `/deputados/{id}/despesas`)
- [ ] **API do Senado Federal** — senadores, matérias, votações
- [ ] **Base dos Dados** — avaliar uso para dados consolidados/históricos
- [ ] Job de sincronização periódica (a API da Câmara é atualizada diariamente) + cache
- [ ] Substituir `data/mock.ts` por dados reais (o próprio arquivo prevê sua descontinuação)
- [ ] Ranking "mais acessados" real (hoje é o campo `acessos` fixo no mock)

---

## 5. Pendências — Inteligência e diferenciais (fase posterior)

Itens discutidos na concepção, ainda não iniciados:

- [ ] **Categorização automática de proposições por tema** (palavras-chave da ementa ou IA) — hoje o tema é preenchido manualmente no mock
- [ ] **Cruzamento automático promessa ↔ ação** — hoje `acaoRelacionada` e `coerenteComDiscurso` são preenchidos à mão; o objetivo é o algoritmo detectar coerência/contradição
- [ ] **Alertas de contradição** — "Fulano prometeu X em 2022 e votou contra Y em 2024"
- [ ] **Frequência em plenário** — presença/ausência em sessões (disponível na API da Câmara)
- [ ] **Linha do tempo** — visualização cronológica promessa → ação
- [ ] **Comparação por estado** — parlamentar vs. média da bancada estadual
- [ ] Evolução do Score de Coerência para versões documentadas (mudanças no algoritmo devem ser registradas no repositório)

---

## 6. Pendências — Design, identidade e infraestrutura

- [~] **Aplicar o `DESIGN_SYSTEM.md` ao código** — tokens CSS, fonte Inter, foco visível, score e componentes principais já foram alinhados; ainda falta revisar a home, footer e componentes legados que mantêm classes `emerald`/`slate`
- [ ] Logo e favicon reais (hoje: badge "PT" em texto e favicon padrão do Next.js)
- [ ] Acessibilidade — revisar contraste conforme tabela WCAG do design system
- [ ] Deploy: Vercel (frontend) + Railway/Render (backend) — sugeridos no README, nada configurado
- [ ] CI/CD (lint, testes, build) — inexistente
- [ ] Atualizar o `AGENTS.md` da raiz — seção 2 ("repositório em fase pré-implementação") está desatualizada: o frontend já existe

---

## 7. Sugestão de ordem de execução

1. **Revisar a home e componentes legados com o design system** — concluir a migração de `emerald`/`slate` para os tokens
2. **Adicionar estados de 404/carregamento, testes unitários e documentação básica** (`.env.example`, READMEs)
3. **Backend + modelo de dados** (seção 3)
4. **Integração com a API da Câmara** (maior valor: dados reais de proposições, votações e gastos)
5. **API do Senado** e moderação real com usuários
6. **Inteligência** (seção 5): categorização automática, cruzamento promessa ↔ ação, alertas
