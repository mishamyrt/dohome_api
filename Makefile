VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

install:
	$(VENV) python setup.py sdist bdist_wheel
	$(VENV) pip3 install .
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
configure:
	python3 -m venv $(VENV_PATH)
	$(VENV) pip3 install -r requirements.txt
lint:
	$(VENV) pylint ./src

