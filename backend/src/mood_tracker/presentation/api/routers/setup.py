from fastapi import APIRouter, FastAPI

from .auth.setup import setup_routers as setup_auth


def setup_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")
    setup_auth(router)

    app.include_router(router)
