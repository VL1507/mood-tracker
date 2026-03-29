.PHONY: test, test-cov, mutant

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src\mood_tracker --cov-report=term-missing --cov-report=html

mutant:
	del cosmic-ray-session.sqlite
	uv run cosmic-ray init cosmic-ray.toml cosmic-ray-session.sqlite
	uv run cosmic-ray exec cosmic-ray.toml cosmic-ray-session.sqlite
	uv run cr-html cosmic-ray-session.sqlite > cosmic-ray-report.html