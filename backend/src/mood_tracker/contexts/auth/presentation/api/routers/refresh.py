from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, HTTPException, Response, status

from mood_tracker.constants import REFRESH_TOKEN_COOKIE_NAME
from mood_tracker.contexts.auth.application.dto.refresh_user import RefreshUserInputDTO
from mood_tracker.contexts.auth.application.use_cases import RefreshUserUseCase
from mood_tracker.contexts.auth.presentation.api.cookie_service import CookieService
from mood_tracker.contexts.auth.presentation.api.schemas.refresh import (
    UserRefreshResponse,
)

router = APIRouter()


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Получение новой пары токенов",
)
@inject
async def refresh(
    response: Response,
    use_case: FromDishka[RefreshUserUseCase],
    cookie_service: FromDishka[CookieService],
    refresh_token: Annotated[
        str | None,
        Cookie(alias=REFRESH_TOKEN_COOKIE_NAME),
    ] = None,
) -> UserRefreshResponse:
    """
    Эндпоинт обновления токенов.

    Returns:
        UserRefreshResponse

    Raises:
        HTTPException: refresh token отсутствует в куки

    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    output_dto = await use_case.execute(
        input_dto=RefreshUserInputDTO(refresh_token=refresh_token),
    )
    cookie_service.set_refresh_token(response=response, token=output_dto.refresh_token)
    return UserRefreshResponse(access_token=output_dto.access_token)
