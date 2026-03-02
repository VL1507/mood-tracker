from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from mood_tracker.application.exceptions import InvalidRefreshTokenError
from mood_tracker.application.use_cases import RefreshUserUseCase
from mood_tracker.presentation.api.cookie_service import CookieService
from mood_tracker.presentation.api.schemas.auth import RefreshLoginResponse

router = APIRouter()


@router.post("/refresh", status_code=status.HTTP_200_OK)
@inject
async def refresh(
    response: Response,
    use_case: FromDishka[RefreshUserUseCase],
    cookie_service: FromDishka[CookieService],
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
) -> RefreshLoginResponse:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    try:
        token_pair = await use_case(refresh_token=refresh_token)
    except InvalidRefreshTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from e

    cookie_service.set_refresh_token(
        response=response, token=token_pair.refresh
    )

    return RefreshLoginResponse(access_token=token_pair.access)
