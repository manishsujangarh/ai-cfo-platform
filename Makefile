.PHONY: api migrate revision upgrade downgrade test format lint docker-up docker-down

api:
	cd apps/api && uv run uvicorn app.main:app --reload

migrate:
	uv run --project apps/api alembic upgrade head

revision:
	uv run --project apps/api alembic revision --autogenerate -m "$(m)"

downgrade:
	uv run --project apps/api alembic downgrade -1

test:
	uv run --project apps/api pytest

format:
	uv run --project apps/api ruff format .

lint:
	uv run --project apps/api ruff check .

docker-up:
	docker compose up -d

docker-down:
	docker compose down