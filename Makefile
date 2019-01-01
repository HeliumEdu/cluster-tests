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
	@if [ "$(OS)" == "Linux" ] ; then make test-selenium ; fi

test-tavern:
	@( \
		source $(CI_VENV)/bin/activate; \
		PYTHONPATH=src/tavern:$$PYTHONPATH pytest -v src/tavern/init/test_setup.tavern.yaml src/tavern/tests/ -s --log-cli-level info; \
	)

test-selenium:
	@( \
		source $(CI_VENV)/bin/activate; \
		PYTHONPATH=src/selenium:$$PYTHONPATH pytest -v src/selenium/tests/ -s; \
	)
