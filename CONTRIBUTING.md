# 🤝 Guia de Contribuição — Política Transparente

Obrigado pelo interesse em contribuir! Este documento explica como você pode participar do projeto de forma organizada e produtiva.

---

## 📋 Índice

1. [Código de Conduta](#código-de-conduta)
2. [Como posso contribuir?](#como-posso-contribuir)
3. [Reportando Bugs](#reportando-bugs)
4. [Sugerindo Funcionalidades](#sugerindo-funcionalidades)
5. [Contribuindo com Código](#contribuindo-com-código)
6. [Cadastrando Promessas](#cadastrando-promessas)
7. [Revisando Pull Requests](#revisando-pull-requests)
8. [Comunicação](#comunicação)

---

## 📜 Código de Conduta

Nosso projeto se compromete a proporcionar uma experiência livre de assédio para todos, independentemente de idade, corpo, deficiência, etnia, identidade de gênero, nível de experiência, nacionalidade, aparência pessoal, raça, religião ou identidade e orientação sexual.

- Seja respeitoso e construtivo
- Aceite críticas com educação
- Foque no que é melhor para a comunidade
- Não tolere comportamentos destrutivos

---

## 💡 Como posso contribuir?

Antes de começar, consulte o [roadmap público](https://github.com/users/paullonorato23/projects/1) e pesquise as Issues abertas. Os status significam:

- **Now**: trabalho priorizado e em execução
- **Next**: próximo conjunto de entregas
- **Later**: ideias aceitas, ainda sem compromisso de prazo

Se você está chegando agora, comece pelas labels [`good first issue`](https://github.com/paullonorato23/politicatransparente/labels/good%20first%20issue) e [`help wanted`](https://github.com/paullonorato23/politicatransparente/labels/help%20wanted). Comente na Issue antes de iniciar para evitar trabalho duplicado.

### Não sabe programar? Sem problema!

| Área | Como ajudar |
|---|---|
| 🗳️ **Dados** | Cadastre promessas de campanha com fonte e verificação |
| 🔍 **Pesquisa** | Encontre fontes oficiais de propostas eleitorais |
| 🎨 **Design** | Sugira melhorias de UX/UI, ícones, ilustrações |
| 📝 **Redação** | Melhore textos, traduções, documentação |
| 📣 **Divulgação** | Compartilhe nas redes, fale com amigos, jornalistas |
| 💰 **Doação** | Ajude com custos de infraestrutura (servidor, domínio) |

---

## 🐛 Reportando Bugs

Encontrou algo errado? Abra uma [Issue](https://github.com/paullonorato23/politicatransparente/issues/new/choose) com o template "Bug Report" e inclua:

1. **Descrição clara** do problema
2. **Passos para reproduzir** (passo a passo)
3. **Comportamento esperado** vs. **comportamento atual**
4. **Screenshots** ou gravações de tela (se aplicável)
5. **Ambiente**: navegador, SO, versão do projeto
6. **Logs** do console (se houver erro)

> 💡 Dica: Verifique se o bug já não foi reportado antes de abrir uma nova issue.

---

## ✨ Sugerindo Funcionalidades

Tem uma ideia? Abra uma [Issue](https://github.com/paullonorato23/politicatransparente/issues/new/choose) com o template "Feature Request":

1. **Qual problema** essa funcionalidade resolve?
2. **Descrição da solução** proposta
3. **Alternativas** consideradas
4. **Contexto adicional** (mockups, referências de outros sites)

---

## 💻 Contribuindo com Código

### 1. Fork e clone
```bash
git clone https://github.com/paullonorato23/politicatransparente.git
cd politicatransparente
```

### 2. Crie uma branch
```bash
git checkout -b tipo/descrição-curta
# Exemplos:
# feature/score-coerencia-algoritmo
# fix/api-camara-timeout
# docs/readme-instalacao
```

### 3. Faça suas alterações
- Siga o estilo de código existente
- Escreva commits claros e descritivos em **português**
- Adicione testes quando aplicável
- Atualize a documentação se necessário

### 4. Commits
Formato sugerido:
```
[tipo] descrição curta

Descrição mais detalhada se necessário.

Refs: #123
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 5. Push e Pull Request
```bash
git push origin sua-branch
```

Abra um PR descrevendo:
- O que foi alterado e por quê
- Como testar
- Issues relacionadas (use `Closes #123`)

Como política de revisão, Pull Requests para `main` devem receber pelo menos uma aprovação de alguém com permissão de escrita no repositório. O autor não pode satisfazer a própria aprovação obrigatória. Revisões da comunidade são bem-vindas e ajudam a decisão, mesmo quando não contam para um requisito técnico de merge. A aplicação automática dessa política depende de configurar branch protection ou um ruleset com *required reviews*.

### Checklist do PR
- [ ] Código compila/roda sem erros
- [ ] Verificações existentes passam (`npm run lint` e `npm run build` no frontend)
- [ ] Não há `console.log` ou debug esquecido
- [ ] Documentação atualizada
- [ ] Commits organizados e descritivos

---

## 🗳️ Cadastrando Promessas

Este é um dos pilares do projeto. Para cadastrar uma promessa:

### Requisitos obrigatórios
1. **Texto exato** da promessa (citação direta quando possível)
2. **Fonte verificável** — link para:
   - Site oficial de campanha (Wayback Machine aceito)
   - Vídeo de debate com timestamp
   - Post oficial em rede social
   - Entrevista em veículo de imprensa
   - Panfleto/santinho digitalizado
3. **Data** da declaração
4. **Categoria temática** (Saúde, Educação, Meio Ambiente, Economia, etc.)
5. **Contexto** — eleição de referência (ex: 2022)

### O que NÃO aceitamos
- ❌ Promessas sem fonte verificável
- ❌ Interpretações ou parafraseamentos sem a citação original
- ❌ Conteúdo de humor, sátira ou meme
- ❌ Informações de menor de idade

### Processo de moderação
1. Usuário cadastra a promessa
2. Sistema verifica link da fonte (status HTTP)
3. Outros usuários podem "validar" ou "questionar" com comentário
4. Após 3 validações ou aprovação de moderador, a promessa é publicada

---

## 🔍 Revisando Pull Requests

Revisar PRs é tão importante quanto escrever código!

### O que avaliar
- [ ] O código faz o que promete?
- [ ] É legível e bem estruturado?
- [ ] Há testes adequados?
- [ ] A documentação foi atualizada?
- [ ] Não introduz dependências desnecessárias?
- [ ] Segue nosso Código de Conduta?

### Como revisar
1. Leia a descrição do PR
2. Teste localmente se possível
3. Deixe comentários construtivos
4. Aprove ou solicite alterações

---

## 💬 Comunicação

- **Issues**: bugs, funcionalidades, discussões técnicas
- **Discussions**: ideias gerais, perguntas, anúncios
- **Pull Requests**: revisão de código

> ⚠️ Evite discussões político-partidárias nos canais técnicos. O projeto é apartidário — nosso foco é transparência de dados, não alinhamento ideológico.

---

## 🙏 Agradecimentos

Toda contribuição, por menor que pareça, fortalece a democracia brasileira. Obrigado por fazer parte!

---

<p align="center">
  <strong>Democracia se fortalece com transparência 🏛️</strong>
</p>
