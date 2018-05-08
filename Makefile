.PHONY: all ci-test

all: ci-test

install:
	python -m pip install -r requirements.txt

ci-test:
	py.test --rootdir=src/tests