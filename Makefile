.PHONY: up down build logs test lint migrate migration shell clean

# ── Docker ──────────────────────────────────────
up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

logs-worker:
	docker compose logs -f worker

restart:
	docker compose restart

ps:
	docker compose ps

# ── Database / Migrations ───────────────────────
migrate:
	docker compose exec api alembic upgrade head

migration:
	docker compose exec api alembic revision --autogenerate -m "$(m)"

rollback:
	docker compose exec api alembic downgrade -1

# ── Tests ───────────────────────────────────────
test:
	docker compose exec api python -m pytest tests/unit -v

test-bdd:
	docker compose exec api python -m pytest tests/bdd -v

test-all:
	docker compose exec api python -m pytest -v

# ── Lint ────────────────────────────────────────
lint:
	docker compose exec api python -m ruff check src/ tests/

lint-fix:
	docker compose exec api python -m ruff check --fix src/ tests/

typecheck:
	docker compose exec api python -m mypy src/

# ── Shell ───────────────────────────────────────
shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec postgres psql -U app -d detections

shell-redis:
	docker compose exec redis redis-cli

# ── Cleanup ─────────────────────────────────────
clean:
	docker compose down -v --rmi local
	if exist "backend\__pycache__" rmdir /s /q "backend\__pycache__"
