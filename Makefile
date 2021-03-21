ROOT_PACKAGE := comparetransactionsets
PYTHON       := python3
ENV_ROOT     := $(shell pwd)/.env
ENV_BIN      := $(ENV_ROOT)/bin
PIP          := $(ENV_BIN)/pip
ISORT        := $(ENV_BIN)/isort
BLACK        := $(ENV_BIN)/black
FLAKE8       := $(ENV_BIN)/flake8
PYTEST       := $(ENV_BIN)/pytest

.PHONY: test build

setup-venv:
	@rm -rf $(ENV_ROOT)
	@$(PYTHON) -m venv $(ENV_ROOT)
	@$(PIP) install --upgrade pip
	@$(PIP) install -e .[test]

check-setup:
	@$(PYTHON) setup.py check

check-imports:
	@$(ISORT) $(ROOT_PACKAGE) test setup.py --check-only

check-formatting:
	@$(BLACK) $(ROOT_PACKAGE) test setup.py --check

format:
	@$(ISORT) $(ROOT_PACKAGE) test setup.py
	@$(BLACK) $(ROOT_PACKAGE) test setup.py

lint:
	@$(FLAKE8) $(ROOT_PACKAGE) test setup.py

test:
	@$(PYTEST) -v --junitxml=test-results/pytest/results.xml
