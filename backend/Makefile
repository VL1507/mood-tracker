.PHONY: format lint test all

format:
	uv run ruff format
	uv run ruff check --fix

lint:
	uv run ruff check
	uv run ty check
	uv run mypy .

test:
	uv run pytest

all: format lint test