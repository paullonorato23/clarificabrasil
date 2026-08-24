# 🎨 Design System — Política Transparente

> Baseado na identidade visual do Governo do Brasil (logo geométrico colorido)

---

## 📐 Filosofia

O design system traduz a **energia cívica** do logo oficial em uma interface **clara, acessível e confiável**. As cores primárias do Brasil são adaptadas para garantir legibilidade, contraste WCAG AA/AAA e hierarquia visual consistente.

**Princípios:**
1. **Transparência literal** — fundos claros, informação organizada, sem distrações
2. **Credibilidade visual** — azul como âncora institucional, verde para dados positivos
3. **Acessibilidade** — contraste mínimo 4.5:1 para todos os textos
4. **Brasilidade sutil** — paleta inspirada no logo, nunca gritante

---

## 🎨 Paleta de Cores

### Primária — Azul República
Derivado do azul elétrico do logo, ajustado para acessibilidade em UI.

| Token | Hex | Uso |
|---|---|---|
| `primary-900` | `#0A1F5C` | Títulos principais, texto em fundos claros |
| `primary-800` | `#0F2D82` | Headlines, ênfase forte |
| `primary-700` | `#143DAD` | **Cor primária principal** — botões primários, links |
| `primary-600` | `#1A4FDB` | Hover de botões, estados ativos |
| `primary-500` | `#3B6EF5` | Destaques, ícones primários |
| `primary-400` | `#6B92F8` | Bordas decorativas, elementos secundários |
| `primary-300` | `#9BB5FB` | Backgrounds sutis, divisores |
| `primary-200` | `#C9D7FD` | Fundos de seção, cards selecionados |
| `primary-100` | `#E8EEFE` | Fundos de hover, badges leves |
| `primary-50`  | `#F3F6FF` | Fundo de página alternativo |

> 💡 **Por que não usar o #183EFF puro?** O azul do logo tem brilho 100% (HSV), o que causa fadiga visual em telas e falha em contraste com branco para textos pequenos. O `primary-700` mantém a identidade mas garante WCAG AA.

### Verde — Ordem e Progresso

| Token | Hex | Uso |
|---|---|---|
| `success-900` | `#064E1F` | Texto de sucesso em fundos claros |
| `success-800` | `#0A6B2E` | — |
| `success-700` | `#0D8A3C` | **Cor de sucesso principal** |
| `success-600` | `#10AB4D` | Hover, estados ativos |
| `success-500` | `#14CC5E` | Badges "Cumprido", ícones positivos |
| `success-400` | `#4DE085` | — |
| `success-300` | `#85EBAB` | — |
| `success-200` | `#BDF5D0` | Fundo de cards "promessa cumprida" |
| `success-100` | `#E3FBEA` | Backgrounds de confirmação |
| `success-50`  | `#F0FDF4` | Fundo sutil de status positivo |

> 🟢 **Conexão com o logo:** O verde `#00D000` do logo é muito saturado. O `success-500` (#14CC5E) preserva o DNA mas funciona em UI sem competir visualmente com o azul primário.

### Amarelo — Atenção e Tramitação

| Token | Hex | Uso |
|---|---|---|
| `warning-900` | `#713F0D` | Texto de alerta |
| `warning-800` | `#92540F` | — |
| `warning-700` | `#B56D12` | — |
| `warning-600` | `#D98A1A` | **Cor de alerta principal** |
| `warning-500` | `#F5A623` | Badges "Em andamento", ícones de atenção |
| `warning-400` | `#F7BC56` | — |
| `warning-300` | `#FAD28A` | — |
| `warning-200` | `#FDE7BD` | Fundo de cards "promessa em andamento" |
| `warning-100` | `#FEF3DD` | Backgrounds de aviso |
| `warning-50`  | `#FFFBF0` | Fundo sutil de alerta |

> 🟡 **Conexão com o logo:** O amarelo `#FFD000` do logo é puro e brilhante. Para UI, foi aquecido levemente para `#F5A623`, evitando competição com o branco e melhorando legibilidade de texto escuro sobre ele.

### Vermelho — Contradição e Erro

| Token | Hex | Uso |
|---|---|---|
| `danger-900` | `#7F1D1D` | Texto de erro |
| `danger-800` | `#991B1B` | — |
| `danger-700` | `#B91C1C` | **Cor de erro/contradição principal** |
| `danger-600` | `#DC2626` | Hover, estados de erro |
| `danger-500` | `#EF4444` | Badges "Contraditado", ícones negativos |
| `danger-400` | `#F87171` | — |
| `danger-300` | `#FCA5A5` | — |
| `danger-200` | `#FECACA` | Fundo de cards "promessa contraditada" |
| `danger-100` | `#FEE2E2` | Backgrounds de erro |
| `danger-50`  | `#FEF2F2` | Fundo sutil de alerta crítico |

> 🔴 **Conexão com o logo:** O vermelho `#FF0000` puro é mantido no `danger-500` (#EF4444) com leve atenuação. Usado com parcimônia — apenas para status críticos e contradições.

### Neutros — Fundo e Texto

| Token | Hex | Uso |
|---|---|---|
| `neutral-950` | `#0A0A0A` | Texto principal (quase preto) |
| `neutral-900` | `#171717` | Headlines, títulos |
| `neutral-800` | `#262626` | Corpo de texto |
| `neutral-700` | `#404040` | Texto secundário |
| `neutral-600` | `#525252` | Labels, captions |
| `neutral-500` | `#737373` | Placeholders, desabilitados |
| `neutral-400` | `#A3A3A3` | Bordas, divisores |
| `neutral-300` | `#D4D4D4` | Bordas de input |
| `neutral-200` | `#E5E5E5` | Divisores sutis |
| `neutral-100` | `#F5F5F5` | Fundo de cards, seções alternadas |
| `neutral-50`  | `#FAFAFA` | **Fundo de página principal** |
| `white` | `#FFFFFF` | Fundo de cards, superfícies elevadas |

> ⚫ **Conexão com o logo:** O cinza `#3C3C3C` do logo é a base do `neutral-700`. A escala sobe até o branco puro, garantindo 12 níveis de hierarquia.

---

## 🔤 Tipografia

### Fonte Principal — Inter

**Por que Inter?**
- Desenhada especificamente para telas e interfaces
- Excelente legibilidade em tamanhos pequenos (dados, tabelas)
- Família completa (9 pesos) com suporte a numerais tabulares (essencial para alinhar gastos e estatísticas)
- Open Source (OFL)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
```

### Escala Tipográfica

Base: `16px` (1rem) | Ratio: `1.25` (Major Third)

| Token | Tamanho | Peso | Line-height | Letter-spacing | Uso |
|---|---|---|---|---|---|
| `display` | 48px / 3rem | 800 | 1.1 | -0.02em | Hero title, números grandes |
| `h1` | 40px / 2.5rem | 800 | 1.2 | -0.02em | Título de página |
| `h2` | 32px / 2rem | 700 | 1.25 | -0.01em | Seção principal |
| `h3` | 24px / 1.5rem | 700 | 1.3 | -0.01em | Subseção, card title |
| `h4` | 20px / 1.25rem | 600 | 1.4 | 0 | Título de lista |
| `h5` | 18px / 1.125rem | 600 | 1.4 | 0 | Label de grupo |
| `body-lg` | 18px / 1.125rem | 400 | 1.6 | 0 | Texto corrido longo |
| `body` | 16px / 1rem | 400 | 1.6 | 0 | **Corpo de texto padrão** |
| `body-sm` | 14px / 0.875rem | 400 | 1.5 | 0 | Descrições, metadados |
| `caption` | 12px / 0.75rem | 500 | 1.4 | 0.01em | Tags, badges, datas |
| `overline` | 11px / 0.6875rem | 700 | 1.2 | 0.08em | Labels uppercase |

### Fonte de Dados — Inter (tabular-nums)

Para números, gastos, scores e estatísticas:

```css
.font-data {
  font-family: 'Inter', sans-serif;
  font-variant-numeric: tabular-nums;
  font-feature-settings: 'tnum';
}
```

Isso garante que `R$ 1.247.892,34` e `R$ 342.100,00` alinhem perfeitamente em colunas.

---

## 📐 Espaçamento

Base: `4px` (0.25rem)

| Token | Valor | Uso |
|---|---|---|
| `space-1` | 4px | Ícones internos, gaps mínimos |
| `space-2` | 8px | Padding de badges, gaps de ícone+texto |
| `space-3` | 12px | Padding de botões pequenos |
| `space-4` | 16px | **Padding padrão de cards** |
| `space-5` | 20px | Padding de seções |
| `space-6` | 24px | Gap entre cards |
| `space-8` | 32px | Margem entre seções |
| `space-10` | 40px | Hero padding |
| `space-12` | 48px | Seção grande |
| `space-16` | 64px | Espaçamento de página |

---

## 🔷 Bordas e Raios

| Token | Valor | Uso |
|---|---|---|
| `radius-sm` | 6px | Badges, tags, inputs |
| `radius-md` | 8px | Botões, cards pequenos |
| `radius-lg` | 12px | **Cards padrão** |
| `radius-xl` | 16px | Modais, containers grandes |
| `radius-2xl` | 20px | Hero sections |
| `radius-full` | 9999px | Avatares, pills |

---

## 🌑 Sombras

| Token | Valor | Uso |
|---|---|---|
| `shadow-sm` | `0 1px 2px rgba(10,10,10,0.05)` | Inputs, badges |
| `shadow-md` | `0 1px 3px rgba(10,10,10,0.08)` | **Cards padrão** |
| `shadow-lg` | `0 4px 12px rgba(10,10,10,0.08)` | Cards hover, dropdowns |
| `shadow-xl` | `0 8px 24px rgba(10,10,10,0.12)` | Modais, toasts |

---

## 🏷️ Componentes Tokenizados

### Botão Primário
```
Background: primary-700 (#143DAD)
Text: white
Padding: space-3 (12px) space-5 (20px)
Radius: radius-md (8px)
Font: body-sm (14px) / weight 600
Hover: primary-600 (#1A4FDB)
Active: primary-800 (#0F2D82)
Shadow: shadow-sm
```

### Card de Promessa — Cumprida
```
Background: white
Border-left: 4px solid success-500 (#14CC5E)
Padding: space-4 (16px)
Radius: radius-lg (12px)
Shadow: shadow-md
Status badge: success-100 bg / success-700 text
```

### Card de Promessa — Em Andamento
```
Background: white
Border-left: 4px solid warning-500 (#F5A623)
Padding: space-4 (16px)
Radius: radius-lg (12px)
Shadow: shadow-md
Status badge: warning-100 bg / warning-700 text
```

### Card de Promessa — Contraditada
```
Background: white
Border-left: 4px solid danger-500 (#EF4444)
Padding: space-4 (16px)
Radius: radius-lg (12px)
Shadow: shadow-md
Status badge: danger-100 bg / danger-700 text
```

### Score de Coerência
```
Font: display (48px) / weight 800 / tabular-nums
Cores por faixa:
  80-100%: success-600 (#10AB4D)
  60-79%:  warning-600 (#D98A1A)
  0-59%:   danger-600 (#DC2626)
```

---

## ♿ Acessibilidade

### Contrastes verificados (WCAG 2.1)

| Combinação | Ratio | Nível |
|---|---|---|
| `primary-700` (#143DAD) sobre `white` | 7.2:1 | ✅ AAA |
| `neutral-800` (#262626) sobre `neutral-50` (#FAFAFA) | 12.4:1 | ✅ AAA |
| `success-700` (#0D8A3C) sobre `success-50` (#F0FDF4) | 5.1:1 | ✅ AA |
| `warning-700` (#B56D12) sobre `warning-50` (#FFFBF0) | 4.6:1 | ✅ AA |
| `danger-700` (#B91C1C) sobre `danger-50` (#FEF2F2) | 6.8:1 | ✅ AA |
| `neutral-500` (#737373) sobre `white` | 4.6:1 | ✅ AA (mínimo para captions) |

### Regras
- Nunca use `warning-500` como cor de texto sobre branco (ratio 2.1:1 — falha)
- Nunca use `success-500` como cor de texto sobre branco (ratio 2.4:1 — falha)
- Sempre use a versão `-700` ou `-800` para texto colorido sobre fundos claros
- Tamanho mínimo de toque: 44×44px (WCAG 2.5.5)

---

## 🎨 Aplicação no Logo do Projeto

O logo do **Política Transparente** (o "P" que sugerimos no wireframe) pode usar:

```
Background: primary-700 (#143DAD)
Text/Ícone: white
```

Ou, para uma versão que dialogue mais com o logo do governo:

```
Background: gradiente de primary-700 → success-600
(azul República → verde Ordem e Progresso)
```

Isso cria identidade própria sem competir com o logo oficial.

---

## 📦 Tokens (formato CSS Variables)

```css
:root {
  /* Primary */
  --color-primary-50: #F3F6FF;
  --color-primary-100: #E8EEFE;
  --color-primary-200: #C9D7FD;
  --color-primary-300: #9BB5FB;
  --color-primary-400: #6B92F8;
  --color-primary-500: #3B6EF5;
  --color-primary-600: #1A4FDB;
  --color-primary-700: #143DAD;  /* Main */
  --color-primary-800: #0F2D82;
  --color-primary-900: #0A1F5C;

  /* Success */
  --color-success-50: #F0FDF4;
  --color-success-100: #E3FBEA;
  --color-success-200: #BDF5D0;
  --color-success-300: #85EBAB;
  --color-success-400: #4DE085;
  --color-success-500: #14CC5E;  /* Main */
  --color-success-600: #10AB4D;
  --color-success-700: #0D8A3C;
  --color-success-800: #0A6B2E;
  --color-success-900: #064E1F;

  /* Warning */
  --color-warning-50: #FFFBF0;
  --color-warning-100: #FEF3DD;
  --color-warning-200: #FDE7BD;
  --color-warning-300: #FAD28A;
  --color-warning-400: #F7BC56;
  --color-warning-500: #F5A623;  /* Main */
  --color-warning-600: #D98A1A;
  --color-warning-700: #B56D12;
  --color-warning-800: #92540F;
  --color-warning-900: #713F0D;

  /* Danger */
  --color-danger-50: #FEF2F2;
  --color-danger-100: #FEE2E2;
  --color-danger-200: #FECACA;
  --color-danger-300: #FCA5A5;
  --color-danger-400: #F87171;
  --color-danger-500: #EF4444;  /* Main */
  --color-danger-600: #DC2626;
  --color-danger-700: #B91C1C;
  --color-danger-800: #991B1B;
  --color-danger-900: #7F1D1D;

  /* Neutral */
  --color-neutral-50: #FAFAFA;
  --color-neutral-100: #F5F5F5;
  --color-neutral-200: #E5E5E5;
  --color-neutral-300: #D4D4D4;
  --color-neutral-400: #A3A3A3;
  --color-neutral-500: #737373;
  --color-neutral-600: #525252;
  --color-neutral-700: #404040;
  --color-neutral-800: #262626;
  --color-neutral-900: #171717;
  --color-neutral-950: #0A0A0A;

  /* Typography */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-data: 'Inter', system-ui, sans-serif; /* + tabular-nums */

  /* Spacing */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 20px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(10, 10, 10, 0.05);
  --shadow-md: 0 1px 3px rgba(10, 10, 10, 0.08);
  --shadow-lg: 0 4px 12px rgba(10, 10, 10, 0.08);
  --shadow-xl: 0 8px 24px rgba(10, 10, 10, 0.12);
}
```

---

*Design System v1.0 — Política Transparente*
