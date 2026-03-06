from fastapi import APIRouter

from . import register


def setup_routers(api_router: APIRouter) -> None:
    router = APIRouter(prefix="/auth", tags=["Auth"])

    router.include_router(register.router)

    api_router.include_router(router)
