from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status

from mood_tracker.application.use_cases import RegisterUserUseCase
from mood_tracker.presentation.api.cookie_service import CookieService
from mood_tracker.presentation.api.schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
@inject
async def register(
    response: Response,
    data: UserRegisterRequest,
    use_case: FromDishka[RegisterUserUseCase],
    cookie_service: FromDishka[CookieService],
) -> UserRegisterResponse:
    token_pair = await use_case(email=data.email, password=data.password)

    cookie_service.set_refresh_token(
        response=response, token=token_pair.refresh
    )

    return UserRegisterResponse(access_token=token_pair.access)
