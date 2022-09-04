CONTAINER_NAME:=fastapi-testing-with-dummy-db
TAG:=$(shell git log -1 --pretty=format:"%H")

.PHONY: build
build: ## Build the docker image.
	docker build \
		$(CACHE_FROM) \
		--build-arg VERSION=$(TAG) \
		--target=release \
		-t $(CONTAINER_NAME) .
	docker build \
		--target=test \
		-t $(CONTAINER_NAME):test .

.PHONY: run
run: ## Run the service using docker-compose.
	docker-compose stop
	docker-compose up

.PHONY: lock-dependencies
lock-dependencies: ## Lock poetry dependencies.
	docker run \
		-v `pwd`:/app \
		-it $(CONTAINER_NAME) poetry lock

.PHONY: lint
lint: ## Run service linting.
	docker run \
		-v $(shell pwd)/src:/app/src \
		-v $(shell pwd)/.pylintrc:/app/.pylintrc \
		$(CONTAINER_NAME) \
		poetry run pylint /app/src

.PHONY: test-clean
test-clean:
	rm -rf tests/cov tests/*.xml tests/.coverage .pytest_cache

.PHONY: test
test: test-clean ## Run service unit tests.
	docker-compose stop
	docker-compose --file docker-compose-test.yaml up --abort-on-container-exit --no-log-prefix

.PHONY: debug
debug: test-clean ## Run service unit tests.
	docker-compose stop
	docker-compose --file docker-compose-test.yaml run $(CONTAINER_NAME)-test \
	/bin/bash -c "pipenv run pytest ${test_dir} -s -v"

.PHONY: create-migration
create-migration: ## Create migration.
	docker-compose run --rm $(CONTAINER_NAME) \
		/bin/bash -c "poetry run alembic revision --autogenerate -m ${desc}"

.PHONY: apply-migrations
apply-migrations: ## Apply migrations.
	docker-compose run --rm $(CONTAINER_NAME) \
		/bin/bash -c "poetry run alembic upgrade head"

.PHONY: downgrade-migrations
downgrade-migrations: ## Apply migrations.
	docker-compose run --rm $(CONTAINER_NAME) \
		/bin/bash -c "poetry run alembic downgrade ${identifier}"
