from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status

from mood_tracker.application.auth.dto.login_user import LoginUserInputDTO
from mood_tracker.application.auth.use_cases import LoginUserUseCase
from mood_tracker.presentation.api.auth.schemas.login import (
    UserLoginRequest,
    UserLoginResponse,
)
from mood_tracker.presentation.api.cookie_service import CookieService

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Вход в аккаунт",
)
@inject
async def login(
    response: Response,
    data: UserLoginRequest,
    use_case: FromDishka[LoginUserUseCase],
    cookie_service: FromDishka[CookieService],
) -> UserLoginResponse:
    output_dto = await use_case(
        input_dto=LoginUserInputDTO(email=data.email, password=data.password),
    )
    cookie_service.set_refresh_token(response=response, token=output_dto.refresh_token)
    return UserLoginResponse(access_token=output_dto.access_token)
