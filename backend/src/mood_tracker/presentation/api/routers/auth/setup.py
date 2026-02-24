from fastapi import APIRouter

from . import register


def setup_routers(app: APIRouter) -> None:
    router = APIRouter(prefix="/auth", tags=["Auth"])
    router.include_router(register.router)

    app.include_router(router)
