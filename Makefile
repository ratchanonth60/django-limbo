COMPOSE_FILE := docker-compose/limbo-dev/docker-compose.yml
COMPOSE_FILE_DEPLOY := docker-compose/deploy/docker-compose.yml

.PHONY: help up down build ssh start stop restart rm ps logs clean list

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

BASE_COMPOSE_CMD = docker-compose -f $(COMPOSE_FILE) 

up: ## Start containers in background
	$(BASE_COMPOSE_CMD) up -d $(target)

down: ## Stop and remove containers, networks, images, and volumes
	$(BASE_COMPOSE_CMD) down

build: ## Build or rebuild services
	$(BASE_COMPOSE_CMD) up -d --build $(target)

ssh: ## SSH into a running container
	$(BASE_COMPOSE_CMD) exec $(target) /bin/bash

start: ## Start services
	$(BASE_COMPOSE_CMD) start $(target)

stop: ## Stop services
	$(BASE_COMPOSE_CMD) stop $(target)

restart: ## Restart services
	$(BASE_COMPOSE_CMD) restart $(target)

rm: ## Remove stopped containers
	$(BASE_COMPOSE_CMD) rm -f $(target)

ps: ## List containers
	$(BASE_COMPOSE_CMD) ps

logs: ## View output from containers
	$(BASE_COMPOSE_CMD) logs -f $(target)

clean: ## Remove all stopped containers, unused networks, images, and build cache
	docker system prune -f

list: ## List all targets
	@$(MAKE) -pRrq -f $(MAKEFILE_LIST) : 2>/dev/null | awk -v RS= -F: ' \
		/^[^.#%][-[:alnum:]_]*:/ { \
		target=$$1; \
		gsub("\n", "", target); \
		gsub(" ", "", target); \
		if (target != "") print target \
		}' | sort

migrate: ## Run a one-off command in a new container
	$(BASE_COMPOSE_CMD) exec limbo python manage.py migrate

tests:
	$(BASE_COMPOSE_CMD) exec limbo pytest --create-db 

debug:
	$(BASE_COMPOSE_CMD) exec limbo echo $POSTGRES_HOST 

tag:
	docker tag $(target) $(image)

push:
	docker push $(image)

deploy:
	docker-compose -f $(COMPOSE_FILE_DEPLOY) up -d --build $(target)
