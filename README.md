# Detection API — FastAPI + YOLO + React

Sistema minimalista de detecção de objetos com arquitetura DDD tático, Docker Compose e frontend React.

## Stack

- **Backend:** FastAPI, SQLAlchemy (async), Alembic, Ultralytics YOLOv8, OpenCV
- **Fila/Cache:** Redis + ARQ worker
- **Banco:** PostgreSQL 16
- **Frontend:** React 19 + Vite
- **Infra:** Docker Compose, nginx (reverse proxy)
- **Auth:** JWT (python-jose, bcrypt)

## Arquitetura

```
backend/src/
├── domain/           # Entities, Value Objects, Repository ABCs, Domain Services
├── application/      # Commands, Queries, Handlers (use cases)
├── infrastructure/   # SQLAlchemy repos, JWT, YOLO, ARQ worker
├── api/              # FastAPI routes, schemas, dependencies
├── config.py         # Settings
└── main.py           # FastAPI app
```

## Como rodar

1. **Clone o projeto:**
   ```sh
   git clone ...
   cd Projeto
   cp .env.example .env
   ```
2. **Build e up:**
   ```sh
   docker compose build
   docker compose up -d
   ```
3. **Migrations:**
   ```sh
   docker compose exec api alembic upgrade head
   ```
4. **Acesse:**
   - Frontend: http://localhost
   - API: http://localhost/api/v1

## Comandos úteis

- `make up` — sobe tudo
- `make down` — derruba tudo
- `make migrate` — aplica migrations
- `make test` — roda testes unitários
- `make test-bdd` — roda testes BDD
- `make lint` — lint com ruff
- `make shell-api` — shell no container api

## Fluxo principal

1. Usuário faz login/registro (JWT)
2. Upload de imagem → cria Detection (PENDING), enfileira job
3. Worker processa, roda YOLO, salva objetos detectados
4. Frontend lista detecções/status

## Estrutura dos commits

- `chore:` inicialização
- `infra:` Docker, configs
- `feat(domain):` camada de domínio
- `feat(application):` camada de aplicação
- `feat(infra):` persistência, auth, worker
- `feat(api):` rotas FastAPI
- `test:` testes unitários e BDD
- `feat(frontend):` React minimalista

## Observações

- Para deploy com GPU, ajuste o Dockerfile para instalar torch com CUDA.
- O frontend só é acessível via nginx na porta 80.
- O backend e worker não expõem portas externas.

---

Feito com SOLID, TDD, BDD e DDD tático. Clean code garantido.
