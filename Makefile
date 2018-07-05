.PHONY: all virtualenv install test

SHELL := /usr/bin/env bash
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
	@( \
		source $(CI_VENV)/bin/activate; \
		PYTHONPATH=src pytest -v src/init/test_setup.tavern.yaml src/tests/ src/init/test_teardown.tavern.yaml -s; \
	)
