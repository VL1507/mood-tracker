from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Response

from mood_tracker.application.use_cases.register_user import (
    RegisterUserUseCase,
)
from mood_tracker.presentation.api.schemas.auth import (
    UserRegisterRequest,
    UserRegisterResponse,
)

router = APIRouter()


@router.post("/register")
async def register(
    response: Response,
    data: UserRegisterRequest,
    use_case: FromDishka[RegisterUserUseCase],
) -> UserRegisterResponse:
    print(data.email, data.password)

    token_pair = await use_case(email=data.email, password=data.password)

    response.set_cookie(
        key="refresh_token",
        value=token_pair.refresh,
        max_age=60 * 60 * 24 * 30,  # TODO: взять значение из конфига
        secure=False,  # TODO: в проде заменить на True
        httponly=True,
        samesite="lax",  # TODO: возможно стоит изменить
    )

    return UserRegisterResponse(access_token=token_pair.access)
