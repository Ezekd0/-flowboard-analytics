# TaskFlow Analytics 📊

A production-ready task management system with advanced analytics capabilities. Built with FastAPI, SQLAlchemy, and modern Python practices.

## 🚀 Features

### Core
- 🔐 JWT Authentication with refresh tokens
- 📝 Full CRUD operations for tasks
- 🗄️ PostgreSQL/SQLite support with connection pooling
- 📚 Auto-generated OpenAPI documentation
- 🛡️ Rate limiting & security headers

### Analytics
- 📈 Real-time productivity metrics
- 🎯 Task completion forecasting
- 📊 User performance ranking
- 🔄 Time-series trend analysis
- 💾 Export reports (JSON/CSV)

### Production Ready
- 🐳 Docker & Docker Compose
- 🔄 Database migrations (Alembic)
- 📝 Structured logging
- 🧪 Unit & integration tests
- ⚡ Redis caching support

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLite for dev)
- **ORM**: SQLAlchemy 2.0
- **Auth**: JWT + bcrypt
- **Analytics**: Pandas, NumPy
- **Testing**: Pytest
- **Deployment**: Docker + GitHub Actions

## 🏃 Quick Start

```bash
# Clone
git clone https://github.com/yourusername/taskflow-analytics.git
cd taskflow-analytics

# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Run
uvicorn app.main:app --reload
```

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Docker (optional)

### Local Development

1. Clone and navigate
```bash
git clone https://github.com/Ezekd0/taskflow-analytics.git
cd taskflow-analytics
```

2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

> Use the local `.venv` environment to avoid system-managed Python restrictions on Linux.

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Copy environment variables
```bash
cp .env.example .env
```

5. Edit `.env` with your values
```bash
nano .env
```

6. Initialize the database
```bash
python scripts/init_db.py
```

7. Seed demo data (optional)
```bash
python scripts/seed_data.py
```

8. Run the application
```bash
uvicorn app.main:app --reload --port 8000
```

Or run directly with Python from the activated environment:
```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

### Docker Setup

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Quick API Examples

### Health check
```bash
curl http://localhost:8000/health
```

### Register user
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_username": "testuser",
    "password": "SecurePass123!"
  }'
```

### Create task
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Build analytics dashboard",
    "description": "Create real-time analytics dashboard",
    "priority": "high",
    "estimated_hours": 8
  }'
```

### Get analytics
```bash
curl -X GET http://localhost:8000/api/v1/analytics/tasks/statistics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Testing

```bash
pytest
pytest --cov=app
```

## License

MIT License
