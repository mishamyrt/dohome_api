VENV_PATH = ./venv
VENV = . $(VENV_PATH)/bin/activate;

configure:
	python3 -m venv $(VENV_PATH)
	$(VENV) pip3 install -r requirements.txt
clean:
	rm -rf $(VENV_PATH)
lint:
	$(VENV) pylint .

