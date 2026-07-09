BIN='mazegenerator.py'
CONF='config.json'

install:
	python3 -m venv pacman_env \
	&& source pacman_env/bin/activate \
	&& pip install -r requirements.txt \
	&& deactivate
run:
	python3 -m venv pacman_env \
	&& source pacman_env/bin/activate \
	&& python3 $(BIN) $(CONF)\
	&& deactivate
debug:
	python -m pdb $(BIN) $(CONF)
clean:
	rm -rf "__pycache__" ".mypy_cache" "mazegen/__pycache__" "solver/__pycache__" ".mypy_cache"
lint:
	flake8 . && mypy . --strict
