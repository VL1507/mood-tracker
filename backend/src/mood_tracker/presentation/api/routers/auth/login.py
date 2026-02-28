from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response

from mood_tracker.application.use_cases import LoginUserUseCase
from mood_tracker.config import Config
from mood_tracker.presentation.api.schemas.auth import (
    UserLoginRequest,
    UserLoginResponse,
)

router = APIRouter()


@router.post("/login")
@inject
async def login(
    response: Response,
    data: UserLoginRequest,
    use_case: FromDishka[LoginUserUseCase],
    config: FromDishka[Config],
) -> UserLoginResponse:
    token_pair = await use_case(email=data.email, password=data.password)

    response.set_cookie(
        key="refresh_token",
        value=token_pair.refresh,
        max_age=config.JWT.REFRESH_EXPIRE_SECONDS,
        secure=False,  # TODO: в проде заменить на True
        httponly=True,
        samesite="lax",  # TODO: возможно стоит изменить
        path="/api/auth",
    )

    return UserLoginResponse(access_token=token_pair.access)
