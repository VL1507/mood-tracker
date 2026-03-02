from fastapi import APIRouter

from . import login, logout, logout_all, refresh, register


def setup_routers(app: APIRouter) -> None:
    router = APIRouter(prefix="/auth", tags=["Auth"])

    router.include_router(login.router)
    router.include_router(logout.router)
    router.include_router(logout_all.router)
    router.include_router(refresh.router)
    router.include_router(register.router)

    app.include_router(router)
