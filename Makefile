PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: install dev test lint format migrate docker-up docker-down clean build

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

dev:
	$(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(PYTHON) -m pytest --cov=app --cov-report=term-missing

lint:
	$(PYTHON) -m flake8 app tests
	$(PYTHON) -m mypy app

format:
	$(PYTHON) -m black app tests scripts
	$(PYTHON) -m isort app tests scripts

migrate:
	$(PYTHON) -m alembic upgrade head

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +

build:
	docker compose -f docker-compose.prod.yml build
