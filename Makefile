include .env
export

MODE ?= dev

ifeq ($(MODE), prod)
    COMPOSE = docker compose -f docker-compose.yml -f docker-compose.prod.yml
else
    COMPOSE = docker compose -f docker-compose.yml -f docker-compose.dev.yml
endif

COMPOSE_TEST = docker compose --env-file .env.test -f docker-compose.yml -f docker-compose.test.yml

.PHONY: up build start stop destroy logs restart shell db cache test coverage coverage-html ci

up:
	$(COMPOSE) up -d --build --remove-orphans

build:
	$(COMPOSE) build

start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

destroy:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f app

restart:
	$(COMPOSE) restart app

shell:
	$(COMPOSE) exec app /bin/bash

db:
	$(COMPOSE) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_NAME"'

cache:
	$(COMPOSE) exec -e REDISCLI_AUTH=$(REDIS_PASSWORD) redis redis-cli

ci:
	@echo "=== Running CI Test pipeline ==="
	$(COMPOSE_TEST) down -v

	$(COMPOSE_TEST) up --build --abort-on-container-exit --exit-code-from sut; \
	EXIT_CODE=$$?; \

	echo "=== [CI] Cleaning up test environment ==="; \
	$(COMPOSE_TEST) down -v; \
	exit $$EXIT_CODE
