from fastapi import APIRouter

from . import login, refresh, register


def setup_routers(api_router: APIRouter) -> None:
    """Подключение роутеров регистрации авторизации /auth."""
    router = APIRouter(prefix="/auth", tags=["Auth"])

    router.include_router(login.router)
    router.include_router(refresh.router)
    router.include_router(register.router)

    api_router.include_router(router)
