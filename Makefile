DOCKER_COMPOSE = docker-compose -f docker/docker-compose.yml

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make build         - Build Docker images"
	@echo "  make up            - Start all containers"
	@echo "  make down          - Stop all containers"
	@echo "  make restart       - Restart all containers"
	@echo "  make logs          - Display logs from all containers"
	@echo "  make migrate       - Run Django migrations"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make shell-backend  - Run shell in backend container"
	@echo "  make shell-api     - Run shell in api container"
	@echo "  make shell-db      - Run MySQL shell"
	@echo "  make clean         - Remove all containers and volumes"

.PHONY: build
build:
	$(DOCKER_COMPOSE) build

.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d
	-$(DOCKER_COMPOSE) exec backend python manage.py collectstatic --noinput
	-$(DOCKER_COMPOSE) exec backend python manage.py migrate

.PHONY: down
down:
	$(DOCKER_COMPOSE) down

.PHONY: restart
restart:
	$(DOCKER_COMPOSE) restart

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

.PHONY: migrate
migrate:
	$(DOCKER_COMPOSE) exec backend python manage.py makemigrations
	$(DOCKER_COMPOSE) exec backend python manage.py migrate

.PHONY: createsuperuser
createsuperuser:
	$(DOCKER_COMPOSE) exec backend python manage.py createsuperuser

.PHONY: shell-backend
shell-backend:
	$(DOCKER_COMPOSE) exec backend bash

.PHONY: shell-api
shell-api:
	$(DOCKER_COMPOSE) exec api bash

.PHONY: shell-db
shell-db:
	$(DOCKER_COMPOSE) exec db mysql -u user -ppassword library

.PHONY: test test-unit test-integration test-coverage test-api

test-backend:
	$(DOCKER_COMPOSE) exec backend python -m pytest library_app/tests/ -v

test-integration:
	$(DOCKER_COMPOSE) exec backend python -m pytest tests/integration/ -v

test-coverage:
	$(DOCKER_COMPOSE) exec backend coverage run -m pytest tests/
	$(DOCKER_COMPOSE) exec backend coverage report
	$(DOCKER_COMPOSE) exec backend coverage html

test-api:
	$(DOCKER_COMPOSE) exec api python -m pytest tests/ -v

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

.PHONY: shell
shell:
	$(DOCKER_COMPOSE) exec backend python manage.py shell

.PHONY: collectstatic
collectstatic:
	$(DOCKER_COMPOSE) exec backend python manage.py collectstatic --noinput

.PHONY: dev
dev:
	$(DOCKER_COMPOSE) up
