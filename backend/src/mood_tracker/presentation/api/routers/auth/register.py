from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Response, status

from mood_tracker.application.dto.register_user import RegisterUserInputDTO
from mood_tracker.application.exceptions import EmailAlreadyExistsError
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
    try:
        output_dto = await use_case(
            context=RegisterUserInputDTO(email=data.email, password=data.email)
        )
    except EmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email is already registered",
        ) from e

    cookie_service.set_refresh_token(
        response=response, token=output_dto.refresh_token
    )

    return UserRegisterResponse(access_token=output_dto.access_token)
