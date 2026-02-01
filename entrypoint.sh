#!/bin/sh

set -e

echo "📦 Running Migrations ..."
alembic upgrade head

echo "🔥 Starting Server ..."
uvicorn src.main:fastapi_app --host 0.0.0.0 --port 8000 --reload
