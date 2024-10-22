.PHONY: all docker-env virtualenv install nopyc clean test test-smoke test-tavern test-tavern-smoke test-selenium test-selenium-smoke build-docker run-docker

SHELL := /usr/bin/env bash
CI_VENV ?= .venv
ENVIRONMENT ?= prod
AWS_REGION ?= us-east-1
PROJECT_APP_HOST ?= https://www.heliumedu.com
PROJECT_API_HOST ?= https://api.heliumedu.com

all: virtualenv install test

docker-env:
	@if [ ! -f ".env" ]; then \
		cp -n .env.docker.example .env | true; \
	fi

virtualenv:
	@if [ ! -d "$(CI_VENV)" ]; then \
		python3 -m pip install virtualenv; \
        python3 -m virtualenv $(CI_VENV); \
	fi

install: virtualenv
	@( \
		source $(CI_VENV)/bin/activate; \
		python -m pip install -r requirements.txt; \
	)

nopyc:
	find . -name '*.pyc' | xargs rm -f || true
	find . -name __pycache__ | xargs rm -rf || true

clean: nopyc
	rm -rf $(CI_VENV)

test:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v src/tavern/test_setup.tavern.yaml src/tavern/tests/ src/tavern/test_teardown.tavern.yaml src/selenium/test_setup.py src/selenium/tests/ src/selenium/test_teardown.py -s --log-cli-level info; \
	)

test-smoke:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v src/tavern/tests/test_api_info.tavern.yaml src/tavern/tests/test_api_status.tavern.yaml src/selenium/tests/test_pages.py src/selenium/tests/test_redirects.py -s --log-cli-level info; \
	)

test-tavern:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v src/tavern/test_setup.tavern.yaml src/tavern/tests/ src/tavern/test_teardown.tavern.yaml -s --log-cli-level info; \
	)

test-selenium:
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v src/selenium/test_setup.py src/selenium/tests/ src/selenium/test_teardown.py -s; \
	)

build-docker:
	docker buildx build -t helium/ci-tests:latest --platform=linux/amd64 --load .

run-docker: docker-env
	docker compose up -d