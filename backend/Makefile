.PHONY: format, lint, test, all, test, test-cov, mutant

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

test-cov:
	uv run pytest --cov=src\mood_tracker --cov-report=term-missing --cov-report=html

mutant:
	del cosmic-ray-session.sqlite
	uv run cosmic-ray init cosmic-ray.toml cosmic-ray-session.sqlite
	uv run cosmic-ray exec cosmic-ray.toml cosmic-ray-session.sqlite
	uv run cr-html cosmic-ray-session.sqlite > cosmic-ray-report.html
	del cosmic-ray-session.sqlite

cognitive:
	uv run complexipy .

cc:
	uv run radon cc src/ -s

mi:
	uv run radon mi src/ -s

hal:
	uv run radon hal src/ 
