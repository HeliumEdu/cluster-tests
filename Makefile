.PHONY: all virtualenv install test

SHELL := /usr/bin/env bash
OS := $(shell uname)
CI_VENV ?= .venv

all: virtualenv install test

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

test:
	@make test-tavern
	ifeq ($(OS),Linux)
		@make test-selenium
	endif;

test-tavern:
	@( \
		source $(CI_VENV)/bin/activate; \
		PYTHONPATH=src pytest -v src/init/test_setup.tavern.yaml src/tests/ src/init/test_teardown.tavern.yaml -s; \
	)

test-selenium:
	@echo "Test Seleium"
