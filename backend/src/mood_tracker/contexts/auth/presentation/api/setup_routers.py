from fastapi import APIRouter, FastAPI

from .routers.setup import setup_routers as setup_auth_routers


def setup_routers(app: FastAPI) -> None:
    """Подключение всех роутеров."""
    router = APIRouter(prefix="/api")

    setup_auth_routers(router)

    app.include_router(router)
