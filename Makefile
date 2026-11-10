COMPOSE = docker compose -f docker-compose.yml -f docker-compose.dev.yml

COMPOSE_TEST = docker compose --env-file .env.test -f docker-compose.yml -f docker-compose.test.yml
CI_SERVICES = db redis minio meilisearch sut

.PHONY: up build start stop destroy logs restart shell db cache test coverage coverage-html ci migration migrate downgrade

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
	$(COMPOSE) logs -f backend

restart:
	$(COMPOSE) restart backend

shell:
	$(COMPOSE) exec backend /bin/bash

db:
	$(COMPOSE) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_NAME"'

cache:
	$(COMPOSE) exec redis sh -c 'redis-cli -a "$$REDIS_PASSWORD"'

migration:
	@test -n "$(m)" || (echo 'Usage: make migration m="message"'; exit 1)
	$(COMPOSE) up -d --wait db
	$(COMPOSE) run --rm --no-deps --entrypoint "" backend \
		alembic revision --autogenerate -m "$(m)"

migrate:
	$(COMPOSE) run --rm --no-deps --entrypoint "" backend alembic upgrade head

downgrade:
	$(COMPOSE) run --rm --no-deps --entrypoint "" backend alembic downgrade -1

ci:
	@echo "=== Running CI Test pipeline ==="
	$(COMPOSE_TEST) down -v
	@$(COMPOSE_TEST) up --build --abort-on-container-exit --exit-code-from sut $(CI_SERVICES); \
	EXIT_CODE=$$?; \
	echo "=== [CI] Cleaning up test environment ==="; \
	$(COMPOSE_TEST) down -v; \
	exit $$EXIT_CODE
