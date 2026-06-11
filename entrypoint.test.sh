#!/bin/sh

set -e

echo "📦 Running Migrations ..."
alembic upgrade head

echo "🌱 Running tests ..."
pytest -v -s

