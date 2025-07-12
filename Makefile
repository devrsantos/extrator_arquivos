run:
	python main.py

test:
	pytest

format:
	black .

lint:
	ruff .

ci: format lint test
