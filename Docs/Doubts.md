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
