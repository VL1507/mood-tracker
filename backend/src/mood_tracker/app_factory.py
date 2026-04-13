from fastapi import FastAPI

from mood_tracker.config import Config
from mood_tracker.presentation.api import (
    setup_exception_handlers,
    setup_routers,
)
from mood_tracker.presentation.api.middleware import setup_middleware
from mood_tracker.presentation.dependencies import setup_di


def create_app() -> FastAPI:
    """
    Создание приложения FastAPI.

    Создается приложение FastAPI, подключаются middleware, routers,
    exception handlers и di

    Returns:
        FastAPI

    """
    config = Config()  # pyright: ignore[reportCallIssue] # ty:ignore[missing-argument]

    app = FastAPI()

    setup_middleware(app=app)
    setup_routers(app=app)
    setup_exception_handlers(app=app)
    setup_di(app=app, config=config)

    return app
