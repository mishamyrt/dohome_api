.PHONY: clean

VERSION = 0.2.6
DIST_PATH = ./dist
VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

SRC := \
	$(wildcard dohome_api/*/*.py) \
	$(wildcard dohome_api/*.py)

.PHONY: publish
publish: clean $(DIST_PATH)
	git tag "v$(VERSION)"
	git push --tags
	$(VENV) python3 -m twine upload --repository pypi dist/* -umishamyrt

.PHONY: clean
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

.PHONY: build
build: $(DIST_PATH)

.PHONY: install
install: $(DIST_PATH)
	pip3 install .

.PHONY: install-venv
install-venv: $(DIST_PATH)
	$(VENV) pip install .

.PHONY: lint
lint:
	$(VENV) pylint $(SRC)

configure: requirements.txt
	rm -rf $(VENV_PATH)
	make $(VENV_PATH)

$(DIST_PATH): $(VENV_PATH) $(SRC)
	echo $(VERSION) > .version
	$(VENV) python3 setup.py sdist bdist_wheel

$(VENV_PATH):
	python3 -m venv $(VENV_PATH)
	$(VENV) pip install -r requirements.txt