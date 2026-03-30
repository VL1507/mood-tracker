from fastapi import APIRouter, FastAPI

from .auth import setup_routers as setup_auth_routers


def setup_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")

    setup_auth_routers(router)

    app.include_router(router)
