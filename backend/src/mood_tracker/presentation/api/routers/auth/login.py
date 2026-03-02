from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status

from mood_tracker.application.use_cases import LoginUserUseCase
from mood_tracker.presentation.api.cookie_service import CookieService
from mood_tracker.presentation.api.schemas.auth import (
    UserLoginRequest,
    UserLoginResponse,
)

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    response: Response,
    data: UserLoginRequest,
    use_case: FromDishka[LoginUserUseCase],
    cookie_service: FromDishka[CookieService],
) -> UserLoginResponse:
    token_pair = await use_case(email=data.email, password=data.password)

    cookie_service.set_refresh_token(
        response=response, token=token_pair.refresh
    )

    return UserLoginResponse(access_token=token_pair.access)
