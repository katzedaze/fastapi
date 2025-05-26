.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Initial setup: copy env file and build containers
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file"; fi
	docker compose build

.PHONY: up
up: ## Start all services
	docker compose up -d

.PHONY: down
down: ## Stop all services
	docker compose down

.PHONY: restart
restart: down up ## Restart all services

.PHONY: logs
logs: ## Show logs from all services
	docker compose logs -f

.PHONY: logs-backend
logs-backend: ## Show backend logs
	docker compose logs -f backend

.PHONY: logs-frontend
logs-frontend: ## Show frontend logs
	docker compose logs -f frontend

.PHONY: shell-backend
shell-backend: ## Open a shell in the backend container
	docker compose exec backend bash

.PHONY: shell-frontend
shell-frontend: ## Open a shell in the frontend container
	docker compose exec frontend sh

.PHONY: shell-db
shell-db: ## Open PostgreSQL shell
	docker compose exec db psql -U postgres -d fastapi_db

.PHONY: migrate
migrate: ## Run database migrations
	docker compose exec backend alembic upgrade head

.PHONY: makemigrations
makemigrations: ## Create a new migration
	docker compose exec backend alembic revision --autogenerate -m "$(m)"

.PHONY: seed
seed: ## Seed the database with dummy data
	docker compose exec backend python scripts/seed_db.py

.PHONY: test
test: ## Run backend tests
	docker compose exec backend pytest

.PHONY: test-cov
test-cov: ## Run backend tests with coverage
	docker compose exec backend pytest --cov=app --cov-report=html

.PHONY: format
format: ## Format backend code with black and ruff
	docker compose exec backend black .
	docker compose exec backend ruff check --fix .

.PHONY: lint
lint: ## Lint backend code
	docker compose exec backend ruff check .
	docker compose exec backend mypy .

.PHONY: clean
clean: ## Clean up containers, volumes, and cache
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

.PHONY: build-prod
build-prod: ## Build production images
	docker build -f backend/Dockerfile -t fastapi-backend:latest backend/
	docker build -f frontend/Dockerfile -t fastapi-frontend:latest frontend/

.PHONY: fresh
fresh: clean setup up migrate seed ## Fresh install: clean, setup, start, migrate, and seed

.PHONY: docs
docs: ## Open API documentation
	@echo "Opening API docs at http://localhost:8000/docs"
	@which xdg-open > /dev/null && xdg-open http://localhost:8000/docs || open http://localhost:8000/docs 2>/dev/null || echo "Please open http://localhost:8000/docs in your browser"
