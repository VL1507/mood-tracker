from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from mood_tracker.application.use_cases import LogoutUserUseCase

router = APIRouter()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout(
    response: Response,
    use_case: FromDishka[LogoutUserUseCase],
    refresh_token: str | None = Cookie(None, alias="refresh_token"),
) -> None:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    response.delete_cookie(
        key="refresh_token",
        path="/api/auth",
    )

    await use_case(refresh_token=refresh_token)
