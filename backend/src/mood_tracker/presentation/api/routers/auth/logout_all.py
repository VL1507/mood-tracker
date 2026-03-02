from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mood_tracker.application.use_cases import LogoutAllUserUseCase

router = APIRouter()
security = HTTPBearer(auto_error=False)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout_all(
    response: Response,
    use_case: FromDishka[LogoutAllUserUseCase],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    access_token = credentials.credentials

    response.delete_cookie(
        key="refresh_token",
        path="/api/auth",
    )

    await use_case(access_token=access_token)
