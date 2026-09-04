#!/bin/sh

set -e

echo "Running Migrations ..."
alembic upgrade head

echo "Running Seeds ..."
python -m scripts.seeds.seed
python -m scripts.search
python -m scripts.seeds.super_admin

echo "Starting Server ..."

if [ "$MODE" = "dev" ]; then
    echo "MODE: DEV"
    exec uvicorn src.main:fastapi_app --host 0.0.0.0 --port 8000 --reload
else
    echo "Mode: ${MODE}"
    exec uvicorn src.main:fastapi_app --host 0.0.0.0 --port 8000
fi
