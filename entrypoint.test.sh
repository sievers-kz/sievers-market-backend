#!/bin/sh

set -e

echo "=== ENV CHECK ==="
echo "POSTGRES_HOST=$POSTGRES_HOST"
echo "POSTGRES_NAME=$POSTGRES_NAME"
echo "POSTGRES_USER=$POSTGRES_USER"
echo "MODE=$MODE"
echo "=== .env file exists? ==="
ls -la /app/.env 2>/dev/null && echo "EXISTS" || echo "NOT FOUND"

echo "📦 Running Migrations ..."
alembic upgrade head

echo "📦 Running Migrations ..."
alembic upgrade head

echo "🌱 Running tests ..."
pytest -v -s

