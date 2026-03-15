#!/bin/bash
set -e

export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"

echo "==> Running database setup..."
python -c "from app.core.database import init_db; init_db()"

echo "==> Starting InvoMatch API..."
python -m gunicorn main:app \
  --workers 1 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --timeout 120 \
  --log-level info
