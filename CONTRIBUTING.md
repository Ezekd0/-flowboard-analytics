# Contributing to TaskFlow Analytics

Thanks for investing time in TaskFlow Analytics. This project aims to model production-grade backend engineering practices, so quality and collaboration standards are intentionally high.

## Development Process

1. Fork the repository and create a branch from `main`.
2. Implement changes with tests and documentation updates.
3. Run quality checks locally before opening a pull request.
4. Open a PR with a clear summary and risk notes.
5. Address review feedback and keep commits focused.

## Local Setup

```bash
git clone https://github.com/[your-username]/taskflow-analytics.git
cd taskflow-analytics
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
cp .env.example .env
```

Run local services:
```bash
docker compose up -d db redis
uvicorn app.main:app --reload --port 8000
```

## Code Quality Standards

- Follow PEP 8 style guidelines.
- Format code with `black` (line length 88).
- Sort imports with `isort`.
- Lint with `flake8`.
- Add and maintain type hints; validate with `mypy`.
- Keep modules cohesive and avoid business logic inside route handlers.

## Testing Requirements

- All changes must include tests when behavior changes.
- Run `pytest --cov=app --cov-report=term-missing`.
- Minimum coverage target: `80%`.
- Add regression tests for every fixed bug.

## Commit Convention

Use Conventional Commits:

- `feat: add analytics trend endpoint`
- `fix: prevent refresh token reuse`
- `docs: update deployment notes`
- `test: add auth integration coverage`
- `chore: upgrade alembic`

## Pull Request Process

1. Rebase branch on latest `main`.
2. Ensure checks pass (`lint`, `type`, `test`).
3. Fill out PR template completely.
4. Link related issues with `Closes #<id>`.
5. Request at least one reviewer.

## Bug Report Template

When reporting bugs, include:
- clear title and concise summary
- reproducible steps
- expected behavior vs actual behavior
- logs, traceback, and relevant payloads
- environment details (OS, Python, DB, Redis versions)

Use the issue template in `.github/ISSUE_TEMPLATE/bug_report.md`.

## Feature Request Template

When proposing features, include:
- problem statement and affected users
- proposed solution and API shape
- alternatives considered
- expected tradeoffs and migration impact

Use the issue template in `.github/ISSUE_TEMPLATE/feature_request.md`.

## Code of Conduct Summary

Participation in this project means following our Code of Conduct. Be respectful, constructive, and inclusive in all interactions. Report concerns privately through channels defined in [CODE_OF_CONDUCT.md](/home/victor/Documents/Port/taskflow-analytics/CODE_OF_CONDUCT.md).
