MODE ?= dev

ifeq ($(MODE), prod)
    COMPOSE = docker-compose -f docker-compose.yml -f docker-compose.prod.yml
else
    COMPOSE = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
endif

COMPOSE_TEST = docker compose --env-file .env.test -f docker-compose.yml -f docker-compose.test.yml

.PHONY: up down clean logs restart shell db test coverage coverage-html

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f app

restart:
	$(COMPOSE) restart app

shell:
	$(COMPOSE) exec app /bin/bash

db:
	$(COMPOSE) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_NAME"'

test:
	$(COMPOSE) exec app pytest -v

coverage:
	$(COMPOSE) exec app pytest --cov=src --cov-report=term-missing

coverage-html:
	$(COMPOSE) exec app pytest --cov=src --cov-report=html

ci:
	@echo "=== Running CI Test pipeline ==="
	$(COMPOSE_TEST) down -v
	$(COMPOSE_TEST) up --build --abort-on-container-exit --exit-code-from sut
	@echo "=== [CI] Cleaning up test environment ==="
	$(COMPOSE_TEST) down -v