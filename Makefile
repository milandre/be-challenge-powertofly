# system python interpreter. used only to create virtual environment
include .env
PY = $(shell which python3)

PYTHON_VERSION_MIN=3.9
PYTHON_VERSION_CUR=$(shell $(PY) -c 'import sys; print("python%d.%d"% sys.version_info[0:2])')
PYTHON_VERSION_OK=$(shell $(PY) -c 'import sys; cur_ver = sys.version_info[0:2]; min_ver = tuple(map(int, "$(PYTHON_VERSION_MIN)".split("."))); print(int(cur_ver >= min_ver))')
ifeq ($(PYTHON_VERSION_OK), 0)
    $(error "Need python version >= $(PYTHON_VERSION_MIN). Current version is $(PYTHON_VERSION_CUR)")
endif

VENV = venv
BIN=$(VENV)/bin
ifeq ($(FLASK_APP), '')
	FLASK_APP=powertofly.py
endif
ifeq ($(FLASK_CONFIG), '')
	FLASK_CONFIG=default
endif

.PHONY: help

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

###################################
### Enviroment Configurations
env-setup: requirements.txt
	$(PYTHON_VERSION_CUR) -m venv $(VENV)

install: env-setup
	$(BIN)/pip3 install -r requirements.txt

###################################
### Docker
docker-compose-up:
	docker-compose up -d

docker-compose-initial-data:
	docker-compose exec powertofly ./init_database.sh

docker-compose-down:
	docker-compose down -v --remove-orphans && docker system prune

docker-compose-test:
	docker-compose exec powertofly python powertofly.py test

###################################
### Flask Dev
initdb: env-setup
	env FLASK_APP="$(FLASK_APP):create_app('$(FLASK_CONFIG)')" $(BIN)/$(PYTHON_VERSION_CUR) -m flask db init

migratedb: env-setup
	env FLASK_APP="$(FLASK_APP):create_app('$(FLASK_CONFIG)')" $(BIN)/$(PYTHON_VERSION_CUR) -m flask db migrate

upgradedb: env-setup
	env FLASK_APP="$(FLASK_APP):create_app('$(FLASK_CONFIG)')" $(BIN)/$(PYTHON_VERSION_CUR) -m flask db upgrade

fakedatadb: env-setup
	env FLASK_APP="$(FLASK_APP):create_app('$(FLASK_CONFIG)')" $(BIN)/$(PYTHON_VERSION_CUR) powertofly.py add-fake-data -n 2000000

test: env-setup
	env FLASK_APP="$(FLASK_APP):create_app('$(FLASK_CONFIG)')" $(BIN)/$(PYTHON_VERSION_CUR) powertofly.py test

pre-commit-install: env-setup
	$(BIN)/pre-commit install

flask: env-setup
	$(BIN)/$(PYTHON_VERSION_CUR) powertofly.py


###################################
### Run local Flask project with
### docker-compose
run-docker-init:
	@$(MAKE) docker-compose-up
	@$(MAKE) docker-compose-initial-data

run-docker: docker-compose-up

run-docker-test: docker-compose-up
	@$(MAKE) docker-compose-test

###################################
### Run local Flask project with
### venv
run-local-init: env-setup
	@$(MAKE) install
	@$(MAKE) migratedb
	@$(MAKE) upgradedb
	@$(MAKE) fakedatadb

run-local: env-setup
	@$(MAKE) install
	@$(MAKE) migratedb
	@$(MAKE) upgradedb
	@$(MAKE) flask

run-local-test: env-setup
	@$(MAKE) test
