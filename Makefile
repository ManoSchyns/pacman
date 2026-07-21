ENV = pacman_env
PYTHON = pacman_env/bin/python
PIP = pacman_env/bin/pip
FLAKE8 = pacman_env/bin/flake8
MYPY = pacman_env/bin/mypy
MAIN = main.py
CONFIG = config.json
PACKAGE = package.sh

MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

install:
	python3 -m venv $(ENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -not -path "./$(ENV)/*" \
		-exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	$(FLAKE8) . && $(MYPY) . $(MYPY_FLAGS)

lint-strict:
	$(FLAKE8) . && $(MYPY) . --strict

package:
	chmod u+x $(PACKAGE)
	. $(ENV)/bin/activate && ./$(PACKAGE) && deactivate

.PHONY: install run debug clean lint lint-strict package
