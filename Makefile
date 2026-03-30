.PHONY: dup ddown ddownv

dup:
	docker compose up --build

ddown:
	docker compose down

ddownv:
	docker compose down -v