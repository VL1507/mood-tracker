from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Response, status

from mood_tracker.application.exceptions import InvalidCredentialsError
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
    try:
        token_pair = await use_case(email=data.email, password=data.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        ) from e

    cookie_service.set_refresh_token(
        response=response, token=token_pair.refresh
    )

    return UserLoginResponse(access_token=token_pair.access)
