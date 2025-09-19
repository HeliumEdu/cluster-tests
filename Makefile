.PHONY: all docker-env install nopyc clean test test-local test-smoke test-tavern test-tavern-smoke test-selenium test-selenium-smoke build-docker run-docker

SHELL := /usr/bin/env bash
PYTHON_BIN ?= python
CI_VENV ?= venv
ENVIRONMENT ?= prod
AWS_REGION ?= us-east-1
PROJECT_APP_HOST ?= https://www.heliumedu.com
PROJECT_API_HOST ?= https://api.heliumedu.com

all: test

docker-env:
	@if [ ! -f ".env" ]; then \
		cp -n .env.docker.example .env | true; \
	fi

venv:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv $(CI_VENV)

install: venv
	@( \
		source $(CI_VENV)/bin/activate; \
		python -m pip install -r requirements.txt; \
	)

nopyc:
	find . -name '*.pyc' | xargs rm -f || true
	find . -name __pycache__ | xargs rm -rf || true

clean: nopyc
	rm -rf $(CI_VENV)

test: install
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v -o junit_suite_name=full src/selenium/test_setup.py src/selenium/test_teardown.py -s --log-cli-level info; \
	)

test-local:
	make -C ../.. build test-ci

test-smoke: install
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v -o junit_suite_name=smoke src/tavern/tests/test_api_info.tavern.yaml src/tavern/tests/test_api_status.tavern.yaml src/selenium/tests/test_pages.py src/selenium/tests/test_redirects.py -s --log-cli-level info; \
	)

test-tavern: install
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v -o junit_suite_name=tavern src/tavern/test_setup.tavern.yaml src/tavern/tests/ src/tavern/test_teardown.tavern.yaml -s --log-cli-level info; \
	)

test-selenium: install
	@( \
		source $(CI_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
		pytest -v -o junit_suite_name=selenium src/selenium/test_setup.py src/selenium/tests/ src/selenium/test_teardown.py -s; \
	)

build-docker:
	docker buildx build -t helium/ci-tests:latest --platform=linux/amd64 --load .

run-docker: docker-env
	docker compose up -d