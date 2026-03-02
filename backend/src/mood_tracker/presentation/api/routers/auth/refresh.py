from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from mood_tracker.application.use_cases import RefreshUserUseCase
from mood_tracker.config import Config
from mood_tracker.presentation.api.schemas.auth import RefreshLoginResponse

router = APIRouter()


@router.post("/refresh")
@inject
async def refresh(
    response: Response,
    use_case: FromDishka[RefreshUserUseCase],
    config: FromDishka[Config],
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
) -> None:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    print(refresh_token)

    token_pair = await use_case(refresh_token=refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=token_pair.refresh,
        max_age=config.JWT.REFRESH_EXPIRE_SECONDS,
        secure=False,  # TODO: в проде заменить на True
        httponly=True,
        samesite="lax",  # TODO: возможно стоит изменить
        path="/api/auth",
    )

    return RefreshLoginResponse(access_token=token_pair.access)
