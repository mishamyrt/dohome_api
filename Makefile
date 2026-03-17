.PHONY: clean

VERSION = 1.1.0
PYTHON_VERSION = 3.13

DIST_PATH = ./dist
VENV_PATH = ./.venv

SRC := \
	$(wildcard dohome_api/*/*.py) \
	$(wildcard dohome_api/*.py)

.PHONY: publish
publish: clean build
	uv run -m twine upload --repository pypi dist/*
	git add Makefile
	git commit -m "chore: release v$(VERSION)"
	git tag "v$(VERSION)"
	git push
	git push --tags

.PHONY: clean
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf "$(DIST_PATH)"
	rm -rf "$(VENV_PATH)"

.PHONY: build
build:
	echo "$(VERSION)" > .version
	uv run -m build

.PHONY: install
install:
	uv pip install .

.PHONY: lint
lint:
	uv run ruff check dohome tests
	uv run pylint dohome tests

.PHONY: test
test:
	uv run pytest -o log_cli=true -vv tests/**/*.py

.PHONY: configure
configure:
	rm -rf $(VENV_PATH)
	uv venv --python $(PYTHON_VERSION)
	uv pip install -e ".[dev]"
	make build
	make install
