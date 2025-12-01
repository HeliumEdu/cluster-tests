.PHONY: all docker-env install nopyc clean test test-local test-smoke test-selenium build-docker run-docker

SHELL := /usr/bin/env bash
PYTHON_BIN ?= python
CLUSTER_VENV ?= venv
ENVIRONMENT ?= prod
AWS_REGION ?= us-east-1
PROJECT_APP_HOST ?= https://www.heliumedu.com
PROJECT_API_HOST ?= https://api.heliumedu.com

ifeq ($(ENVIRONMENT), prod)
    ENVIRONMENT_PREFIX := ""
else
    ENVIRONMENT_PREFIX := "$(ENVIRONMENT)."
endif

all: test

docker-env:
	@if [ ! -f ".env" ]; then \
		cp -n .env.docker.example .env | true; \
	fi

venv:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv $(CLUSTER_VENV)

install: venv
	@( \
		source $(CLUSTER_VENV)/bin/activate; \
		python -m pip install -r requirements.txt; \
	)

nopyc:
	find . -name '*.pyc' | xargs rm -f || true
	find . -name __pycache__ | xargs rm -rf || true

clean: nopyc
	rm -rf $(CLUSTER_VENV)

test-local:
	make -C ../.. build test-cluster

test: test-smoke test-selenium

test-smoke: install
	@( \
		source $(CLUSTER_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		ENVIRONMENT_PREFIX=$(ENVIRONMENT_PREFIX) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
			pytest -o junit_suite_name=tavern \
			src/tavern/test_setup.tavern.yaml src/tavern/tests/ src/tavern/test_teardown.tavern.yaml \
			--log-cli-level info --tavern-global-cfg src/tavern/common.yaml; \
	)

test-selenium: install
	@( \
		source $(CLUSTER_VENV)/bin/activate; \
		ENVIRONMENT=$(ENVIRONMENT) \
		ENVIRONMENT_PREFIX=$(ENVIRONMENT_PREFIX) \
		AWS_REGION=$(AWS_REGION) \
		PROJECT_APP_HOST=$(PROJECT_APP_HOST) \
		PROJECT_API_HOST=$(PROJECT_API_HOST) \
			pytest -o junit_suite_name=selenium \
			--reruns 2 --reruns-delay 5 \
			src/selenium/test_setup.py src/selenium/tests/ src/selenium/test_teardown.py; \
	)

build-docker:
	docker buildx build -t helium/cluster-tests:latest --platform=linux/amd64 --load .

run-docker: docker-env
	docker compose up -d