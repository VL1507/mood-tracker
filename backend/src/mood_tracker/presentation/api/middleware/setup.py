from fastapi import FastAPI

from .logging_middleware import LoggingMiddleware


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(LoggingMiddleware)
