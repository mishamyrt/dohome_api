.PHONY: clean

VERSION = 1.0.1
DIST_PATH = ./dist
PYTHON_BIN = python3.13
VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

SRC := \
	$(wildcard dohome_api/*/*.py) \
	$(wildcard dohome_api/*.py)

.PHONY: publish
publish: clean $(DIST_PATH)
	git tag "v$(VERSION)"
	git push --tags
	$(VENV) python -m twine upload --repository pypi dist/* -umishamyrt

.PHONY: clean
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

.PHONY: build
build:
	echo "$(VERSION)" > .version
	$(VENV) python -m build

.PHONY: install
install:
	$(VENV) pip install .
	$(VENV) pipx install .

.PHONY: lint
lint:
	$(VENV) ruff check dohome_api
	$(VENV) pylint dohome_api

.PHONY: test
test:
	$(VENV) pytest -o log_cli=true -vv tests/*.py

.PHONY: configure
configure:
	rm -rf $(VENV_PATH)
	$(PYTHON_BIN) -m venv $(VENV_PATH)
	$(VENV) pip install -r requirements.txt
