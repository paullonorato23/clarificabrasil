# Dúvidas e decisões de projeto

> Registro das dúvidas que surgiram durante a implementação e das decisões
> tomadas para não bloquear o andamento. Itens marcados como **aberto**
> aguardam decisão do mantenedor.

---

## Backend (sessão de 25/08/2026)

### 1. Ambiente local de Python — **aberto**
O README exige Python 3.11+, mas a máquina de desenvolvimento só tinha
Python 3.9.6 (sistema) e Homebrew. Pergunta enviada ao mantenedor com as
opções: instalar `python@3.12` via Homebrew, usar o 3.9 mesmo, ou apenas
entregar o código sem executar os testes localmente.
*Enquanto isso, o código foi escrito compatível com 3.9+ (sem sintaxe 3.10+
fora de anotações) e a suíte foi executada em venv local.*

### 2. Promessa com link de fonte quebrado — decidido (revisável)
A concepção prevê "verificação automática do link da fonte (status HTTP)",
mas não diz o que fazer quando o link falha. **Decisão:** a promessa é criada
normalmente, marcada com `fonte_verificada=false` e o status HTTP observado;
a moderação (comunidade + moderadores) decide o destino. Alternativa seria
rejeitar o cadastro com 422 — mais rígido, mas puniria fontes temporariamente
fora do ar. Revisar se a comunidade preferir rigidez no cadastro.

### 3. Rejeição de paráfrases, sátira e conteúdo envolvendo menores — decidido
A concepção lista esses motivos de rejeição, mas não são verificáveis
automaticamente sem processamento de linguagem. **Decisão:** ficam a cargo do
moderador, com `motivo` obrigatório na rejeição (a API grava o motivo).
A detecção automática entra na fase de "Inteligência" (seção 5 das pendências).

### 4. Login em JSON vs. formulário OAuth2 — decidido
O login usa JSON (`{"email", "senha"}`) em vez do formulário
`application/x-www-form-urlencoded` do padrão OAuth2, por ser mais simples de
consumir no frontend. O token é bearer JWT no header `Authorization`.

### 5. Criação de moderadores — **aberto**
Hoje o moderador inicial é criado via variáveis de ambiente
(`ADMIN_EMAIL`/`ADMIN_SENHA`) no startup. Não há endpoint para promover um
usuário comum a moderador — assumido como operação administrativa manual
(direto no banco) nesta fase. Definir se haverá painel de administração.

### 6. Promessas rejeitadas na consulta individual — decidido
`GET /promessas/{id}` restringe ao autor e a moderadores tanto promessas
pendentes quanto rejeitadas (o motivo da rejeição pode conter avaliação
editorial interna). Apenas promessas **publicadas** são públicas.

### 7. Score de Coerência — decidido
A fonte da verdade da v0.1 era o frontend (`frontend/src/lib/score.ts`).
O backend portou a fórmula exata (`backend/app/score.py`) e passa a ser a
fonte canônica quando o frontend migrar para dados reais. Versões futuras
devem ser documentadas aqui e na rota `/metodologia`.

### 12. Base dos Dados: usar ou não? — decidido (26/08/2026)
Avaliação completa em `Docs/Base-dos-Dados.md` (issue #27). **Decisão: usar
como fonte complementar, não primária** — backfill histórico (despesas desde
1959, votações desde 1934) e frequência em plenário (`evento_presenca_deputado`).
A API oficial da Câmara segue como fonte primária dos dados correntes.
A BD **não cobre o Senado** — a API do Senado (issue #9) continua necessária.
*(Numerada como 12 porque os itens 8–11 estão no PR #22, ainda aberto.)*
---

## Moderação e transparência (sessão de 25/08/2026, tarde)

### 8. Visibilidade total da moderação — decidido (a implementar)
O mantenedor decidiu que a moderação deve ser **100% transparente**: qualquer
visitante (mesmo sem login) poderá ver promessas pendentes, publicadas e
rejeitadas **com o motivo da rejeição**. Isso muda o comportamento atual da
API (hoje `GET /promessas/{id}` restringe pendentes/rejeitadas a autor e
moderadores) e pede uma UX própria (abas por situação no perfil do
parlamentar, em definição). A fila de moderação segue exigindo login para
**agir** (validar/questionar), mas não para **ver**.

### 9. Moderador não modera o próprio envio — decidido e **implementado**
Ninguém — nem moderadores — pode aprovar/rejeitar uma promessa que enviou
(regra `_impede_automoderacao` em `backend/app/routers/moderacao.py`,
testes em `test_moderacao.py`). A promessa de um moderador só pode ser
moderada pela comunidade ou por outro moderador.

### 10. Snapshot da fonte — decidido (a implementar)
Para provar que a fala existiu mesmo se a página sair do ar: arquivar a URL
no momento do cadastro. Caminho preferido: **API do Wayback Machine**
(`https://archive.org/wayback/available` para consultar e
`https://web.archive.org/save/<url>` para arquivar), sem custo e sem conta.
A UX deve esconder a complexidade: o usuário só cola o link; o sistema
arquiva e guarda a URL do snapshot. Complemento: campo "citação literal" da
fala, conferido pelo moderador contra o snapshot.

### 11. Reputação progressiva — decidido (a especificar)
Aprovada a ideia de contas com limites crescentes conforme histórico de
contribuições aprovadas. A regra deve ser **pública** (página no site), como
a metodologia do Score. Especificação fica para a fase anti-abuso
(prioridade 0).

*(O item 12 — avaliação da Base dos Dados — está no PR #35, aguardando merge.)*

---

## Integração Câmara (sessão de 27/08/2026)

### 13. Tipos de proposição importados — decidido
A Câmara tem dezenas de tipos (MPV, PLP, PDL, RIC...), mas o enum do frontend
só conhece PL, PEC e REQ. **Decisão:** a sincronização importa apenas esses
três tipos. Revisar quando o frontend suportar mais tipos.

### 14. Tema de proposições e votações importadas — decidido
A classificação temática da Câmara não corresponde aos nossos 8 temas.
**Decisão:** `tema` fica **nulo** nos registros importados até a
categorização automática (issue #28). O campo passou a ser opcional no modelo
e nos schemas.

### 15. Coerência e votos não efetivos — decidido
- `coerente_com_discurso` é avaliação **editorial** — a API não a fornece.
  Votos importados ficam com `None` e o Score v0.1 passou a **ignorar votos
  não avaliados** (esclarecimento documentado em `app/score.py` e testado).
- Tipos de voto da Câmara que não são Sim/Não/Abstenção ("Não votou",
  "Obstrução", "Presente", "Branco"...) viram **Ausente** no nosso enum.
