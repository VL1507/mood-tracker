from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mood_tracker.application.use_cases import LogoutAllUserUseCase
from mood_tracker.presentation.api.cookie_service import CookieService

router = APIRouter()
security = HTTPBearer(auto_error=False)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout_all(
    response: Response,
    use_case: FromDishka[LogoutAllUserUseCase],
    cookie_service: FromDishka[CookieService],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    access_token = credentials.credentials

    cookie_service.delete_refresh_token(response=response)

    await use_case(access_token=access_token)
