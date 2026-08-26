# Backend — Política Transparente

API REST em FastAPI que alimenta o frontend: parlamentares, promessas de campanha
com moderação colaborativa, proposições, votações, gastos e o Score de Coerência (v0.1).

## Requisitos

- Python 3.11+
- PostgreSQL 15+ (produção). Para desenvolvimento rápido, o padrão é SQLite
  (basta não definir `DATABASE_URL`).

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env      # edite conforme o ambiente
uvicorn main:app --reload # http://localhost:8000 (docs em /docs)
```

## Testes

```bash
pytest
```

Os testes rodam em SQLite em memória e não precisam de PostgreSQL nem de rede
(a verificação HTTP de fontes é mockada).

## Estrutura

```
main.py            # entrypoint (uvicorn main:app), CORS, startup, /health
app/
  config.py        # configurações via .env (pydantic-settings)
  database.py      # engine, sessão e Base do SQLAlchemy
  enums.py         # enums de domínio (mesmos valores do frontend)
  models.py        # modelos SQLAlchemy
  schemas.py       # schemas Pydantic (JSON em camelCase)
  security.py      # hash de senha (argon2) e JWT
  deps.py          # dependências: get_db, usuário autenticado, moderador
  score.py         # Score de Coerência v0.1 (metodologia pública e versionada)
  fontes.py        # verificação do link da fonte (status HTTP)
  seed.py          # criação do moderador inicial via env
  routers/         # auth, parlamentares, promessas, moderacao
tests/             # pytest
```
