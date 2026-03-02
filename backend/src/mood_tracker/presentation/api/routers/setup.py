from fastapi import APIRouter, FastAPI


def setup_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")

    app.include_router(router)
