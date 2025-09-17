lint:
	pylint --rcfile .pylintrc frontend backend
	mypy --config-file setup.cfg .
	black --check --config black.toml .

format:
	black --verbose --config black.toml .
	isort --sp .isort.cfg .

