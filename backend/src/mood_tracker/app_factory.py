from fastapi import FastAPI

from mood_tracker.config import Config
from mood_tracker.presentation.api import (
    setup_exception_handlers,
    setup_routers,
)
from mood_tracker.presentation.dependencies import setup_di


def create_app() -> FastAPI:
    config = Config()  # ty:ignore[missing-argument]

    app = FastAPI()

    setup_routers(app=app)
    setup_exception_handlers(app=app)
    setup_di(app=app, config=config)

    return app
