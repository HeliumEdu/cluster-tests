.PHONY: all install test

all: install test

install:
	python -m pip install -r requirements.txt

test:
	PYTHONPATH=src pytest -v src/init/test_setup.tavern.yaml src/tests/ src/init/test_teardown.tavern.yaml -s