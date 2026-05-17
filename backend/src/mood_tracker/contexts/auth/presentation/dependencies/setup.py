from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from mood_tracker.config import Config

from .container import make_container_di


def setup_di(app: FastAPI, config: Config) -> None:
    """Подключение dishka к FastAPI."""
    container = make_container_di(config=config)
    setup_dishka(container=container, app=app)
