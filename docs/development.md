# Development Setup

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

## Quick Start (Docker)

```bash
# Clone the repo
git clone https://github.com/your-org/invomatch.git
cd invomatch

# Copy env file
cp backend/.env.example backend/.env

# Start all services
docker-compose up --build

# API docs available at:
# http://localhost:8000/api/docs

# Frontend at:
# http://localhost:3000
```

## Local Backend (without Docker)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements/dev.txt

# Set environment variables
export DATABASE_URL="postgresql://invo_match:devpass@localhost/invo_match"
export REDIS_URL="redis://localhost:6379"
export SECRET_KEY="local-dev-secret"

# Run database migrations
python -c "from app.core.database import init_db; init_db()"

# Start API
uvicorn app.main:app --reload
```

## Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires Postgres + Redis)
pytest tests/integration -v

# All tests with coverage
pytest tests/unit tests/integration --cov=app --cov-report=html

# E2E tests (requires running app)
npx playwright test
```

## Git Workflow

```
main       ← production, protected
develop    ← integration branch
feature/*  ← feature development
hotfix/*   ← urgent production fixes
```

```bash
# Start a feature
git checkout develop
git checkout -b feature/your-feature-name
git commit -m "feat(module): description"
git push origin feature/your-feature-name
# Open PR → develop
```

## Commit Convention

```
feat(invoices): add background verification task
fix(payments): resolve rounding error on reconciliation
refactor(users): extract token logic to security module
test(clients): add integration test for delete endpoint
docs: update architecture diagram
```
