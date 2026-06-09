#!/bin/sh

set -e

echo "📦 Running Migrations ..."
alembic upgrade head

echo "🌱 Running Seeds ..."
python -m scripts.seeds.seed

echo "🔥 Starting Server ..."
uvicorn src.main:fastapi_app --host 0.0.0.0 --port 8000 --reload
