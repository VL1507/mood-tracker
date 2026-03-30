from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status

from mood_tracker.application.auth.dto.register_user import (
    RegisterUserInputDTO,
)
from mood_tracker.application.auth.use_cases import RegisterUserUseCase
from mood_tracker.presentation.api.auth.schemas.register import (
    UserRegisterRequest,
    UserRegisterResponse,
)
from mood_tracker.presentation.api.cookie_service import CookieService

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
)
@inject
async def register(
    response: Response,
    data: UserRegisterRequest,
    use_case: FromDishka[RegisterUserUseCase],
    cookie_service: FromDishka[CookieService],
) -> UserRegisterResponse:
    output_dto = await use_case.execute(
        input_dto=RegisterUserInputDTO(email=data.email, password=data.password),
    )
    cookie_service.set_refresh_token(response=response, token=output_dto.refresh_token)
    return UserRegisterResponse(access_token=output_dto.access_token)
