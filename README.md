# Política Transparente 🇧🇷

> **O que seu representante prometeu vs. o que ele realmente fez?**

Plataforma colaborativa e sem fins lucrativos para monitorar a atuação de deputados federais e senadores brasileiros durante seus mandatos. Cruzamos promessas de campanha com proposições, votações e gastos — tudo com dados oficiais e código aberto.

---

## ✨ O que faz

| Funcionalidade | Descrição |
|---|---|
| 📋 **Promessas de Campanha** | Cadastro colaborativo de propostas eleitorais com fonte e verificação |
| 📜 **Proposições** | Acompanhamento automático de PLs, PECs e requerimentos via API oficial |
| 🗳️ **Votações** | Registro de votações nomeadas com análise de coerência vs. discurso |
| 💰 **Gastos do Gabinete** | Transparência sobre despesas parlamentares em tempo real |
| 📊 **Score de Coerência** | Índice que mede o alinhamento entre promessas e ações |
| ⚖️ **Comparador** | Compare lado a lado a atuação de diferentes parlamentares |

---

## 🗂️ Fontes de Dados

Todas as informações são extraídas de fontes oficiais e abertas:

- **[API Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/)** — proposições, votações, deputados, gastos
- **[API do Senado Federal](https://www12.senado.leg.br/dados-abertos)** — projetos, tramitações, senadores
- **[Base dos Dados](https://basedosdados.org/)** — dados consolidados e tratados para análise

> ⚠️ As **promessas de campanha** são cadastradas pela comunidade com link da fonte original (entrevista, site oficial, debate, panfleto etc.) e passam por moderação antes de serem publicadas.

---

## 🚀 Tecnologias

```
Frontend:  React / Next.js / TailwindCSS
Backend:   Python / FastAPI
Banco:     PostgreSQL
Dados:     APIs oficiais da Câmara e Senado + Base dos Dados
Deploy:    (a definir — Vercel + Railway/Render sugeridos)
```

---

## 🛠️ Como rodar localmente

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/politica-transparente.git
cd politica-transparente
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edite .env com suas credenciais do PostgreSQL
uvicorn main:app --reload
```

### 3. Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Acesse: `http://localhost:3000`

---

## 🤝 Como contribuir

Adoramos contribuições! Seja código, design, dados, revisão de promessas ou divulgação.

Leia nosso [CONTRIBUTING.md](CONTRIBUTING.md) para o passo a passo completo.

Formas rápidas de ajudar:
- 🐛 Reporte bugs em [Issues](https://github.com/seu-usuario/politica-transparente/issues)
- 💡 Sugira funcionalidades
- 📝 Cadastre e verifique promessas de campanha
- 🔍 Revise pull requests
- 📣 Divulgue o projeto

---

## 🏛️ Governança

Este projeto é **sem fins lucrativos**, de código aberto e mantido por voluntários. Não aceitamos financiamento de partidos políticos, empresas com interesses legislativos ou qualquer entidade que possa comprometer nossa independência.

Nossa metodologia de cálculo do *Score de Coerência* é pública, auditável e versionada neste repositório.

---

## 📜 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">
  Feito com ❤️ e ☕ pelo povo brasileiro<br>
  <strong>Democracia se fortalece com transparência</strong>
</p>
