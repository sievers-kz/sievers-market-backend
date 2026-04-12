up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f app

restart:
	docker-compose restart app

shell:
	docker-compose exec app /bin/bash

db:
	docker-compose exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_NAME"'

test:
	docker-compose exec app pytest -v

coverage:
	docker-compose exec app pytest --cov=src --cov-report=term-missing

coverage-html:
	docker-compose exec app pytest --cov=src --cov-report=html

seed:
	docker-compose exec app python -m fixtures.seed

clean-seed:
	docker-compose exec app python -m fixtures.clean

clean:
	docker-compose down -v
