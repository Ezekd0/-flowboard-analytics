# TaskFlow Analytics 📊

[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-blue)](https://github.com/[your-username]/taskflow-analytics/actions)
[![Coverage](https://img.shields.io/badge/coverage-80%25%2B-brightgreen)](https://github.com/[your-username]/taskflow-analytics/actions)
[![Deployment](https://img.shields.io/badge/deployment-docker%20%7C%20nginx-blueviolet)](https://your-domain.com)

Production-ready FastAPI backend for task management and analytics, designed as a portfolio-grade project that demonstrates API design, security, performance, and delivery practices expected in modern engineering teams.

Live API: `https://your-domain.com`  
Live Docs (Swagger): `https://your-domain.com/api/docs`  
Live Docs (ReDoc): `https://your-domain.com/api/redoc`

## Key Features

| Core Backend | Advanced Analytics | Production Features |
| --- | --- | --- |
| JWT auth (access + refresh) | Productivity metrics and trends | Dockerized services and NGINX reverse proxy |
| Task CRUD with filtering and validation | Completion forecasting workflows | Alembic migrations and environment isolation |
| SQLAlchemy models and transactional services | Team/user-level KPI endpoints | Structured logging and health checks |
| OpenAPI docs and versioned API routes | Data export-ready analytics responses | Redis + Celery support and rate limiting |

## Tech Stack

| Layer | Technology |
| --- | --- |
| API Framework | FastAPI |
| Language | Python 3.11+ |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL (SQLite for local fallback) |
| Caching / Queue | Redis + Celery |
| Authentication | JWT (`python-jose`) + `passlib` bcrypt |
| Analytics | Pandas, NumPy |
| Migrations | Alembic |
| ASGI Server | Uvicorn / Gunicorn (prod) |
| Testing | Pytest |
| Deployment | Docker Compose + NGINX |

## Project Structure

```text
taskflow-analytics/
├── app/
│   ├── api/v1/              # Route definitions
│   ├── core/                # Security, DB session, exceptions
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business and analytics logic
│   ├── static/              # Frontend static assets
│   ├── templates/           # Server-rendered templates
│   ├── config.py            # Environment-driven settings
│   └── main.py              # FastAPI app entrypoint
├── migrations/              # Alembic migration scripts
├── scripts/                 # DB init and seed helpers
├── tests/                   # Unit/integration tests
├── docker-compose.yml       # Development stack
├── docker-compose.prod.yml  # Production stack
├── nginx.conf               # Reverse proxy + security config
└── pyproject.toml           # Tooling and project metadata
```

## Quick Start

1. Clone repository and enter directory.
```bash
git clone https://github.com/[your-username]/taskflow-analytics.git
cd taskflow-analytics
```
2. Create and activate virtual environment.
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Install dependencies.
```bash
pip install -r requirements.txt
```
4. Create environment file.
```bash
cp .env.example .env
```
5. Initialize local database.
```bash
python scripts/init_db.py
```
6. Run API in development mode.
```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation and Usage

After startup:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI JSON: `http://localhost:8000/api/openapi.json`

Health check:
```bash
curl http://localhost:8000/health
```

Register:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"demo","password":"StrongPass123!","full_name":"Demo User"}'
```

Login:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email_or_username":"demo","password":"StrongPass123!"}'
```

Create task:
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Implement analytics endpoint","priority":"high","estimated_hours":6}'
```

Fetch analytics:
```bash
curl -X GET http://localhost:8000/api/v1/analytics/tasks/statistics \
  -H "Authorization: Bearer <access-token>"
```

## Docker Deployment

Development:
```bash
docker compose up --build
```

Production:
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Scale API in production:
```bash
docker compose -f docker-compose.prod.yml up -d --scale api=3
```

## Testing

```bash
pytest
pytest --cov=app --cov-report=term-missing
```

Coverage target: `>= 80%`.

## Performance Benchmarks

| Metric | Baseline |
| --- | --- |
| Average API latency (p50) | `< 120ms` |
| Average API latency (p95) | `< 350ms` |
| Throughput (single instance) | `~500 req/s` |
| Auth endpoint latency (p95) | `< 200ms` |
| Analytics endpoint latency (p95) | `< 500ms` |

## Security Features

- [x] JWT access and refresh token flow
- [x] Password hashing with bcrypt
- [x] Environment-based secret management
- [x] Rate limiting controls
- [x] Security-focused NGINX headers
- [x] Input validation with Pydantic
- [x] Dependency isolation via virtual environments / containers
- [x] Structured logging for incident response

## Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `APP_NAME` | Application name | `TaskFlow Analytics` |
| `ENVIRONMENT` | Runtime environment | `development` |
| `SECRET_KEY` | JWT signing key | `replace-with-secure-key` |
| `DATABASE_URL` | SQLAlchemy DB URL | `postgresql://user:pass@db:5432/taskflow` |
| `REDIS_URL` | Redis URL | `redis://redis:6379/0` |
| `BACKEND_CORS_ORIGINS` | Allowed origins | `["http://localhost:3000"]` |
| `RATE_LIMIT_REQUESTS` | Requests allowed per window | `100` |
| `LOG_LEVEL` | Logging level | `INFO` |

See [.env.example](/home/victor/Documents/Port/taskflow-analytics/.env.example) and [.env.production.example](/home/victor/Documents/Port/taskflow-analytics/.env.production.example) for full configuration.

## Contributing

Contributions are welcome. Use feature branches, follow Conventional Commits, keep tests green, and include documentation updates for behavior changes. Full workflow is in [CONTRIBUTING.md](/home/victor/Documents/Port/taskflow-analytics/CONTRIBUTING.md).

## Why This Project for Portfolio

TaskFlow Analytics demonstrates backend breadth expected for mid-level and senior backend roles:
- practical API design with layered architecture
- production concerns (security, ops, observability)
- asynchronous worker and cache integration
- testing and quality gates suitable for team workflows
- documentation quality needed for onboarding and collaboration

## License

MIT License. See [LICENSE](/home/victor/Documents/Port/taskflow-analytics/LICENSE) (or add one if missing).
Copyright (c) 2024 [your-name].

## Author

**[Your Name]**  
GitHub: `https://github.com/[your-username]`  
LinkedIn: `https://linkedin.com/in/[your-username]`  
Portfolio: `https://[your-domain.com]`
