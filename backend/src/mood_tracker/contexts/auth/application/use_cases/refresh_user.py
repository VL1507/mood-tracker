import structlog

from mood_tracker.contexts.auth.application.dto.refresh_user import (
    RefreshUserInputDTO,
    RefreshUserOutputDTO,
)
from mood_tracker.contexts.auth.application.exceptions import InvalidRefreshTokenError
from mood_tracker.contexts.auth.domain.security import ITokenService

logger = structlog.stdlib.get_logger()


class RefreshUserUseCase:
    """Use case обновления токенов пользователя."""

    def __init__(self, token_service: ITokenService) -> None:
        """Инициализирует use case обновления токенов пользователя."""
        self._token_service = token_service

    async def execute(self, input_dto: RefreshUserInputDTO) -> RefreshUserOutputDTO:
        """
        Принимает старый refresh token и возвращает новую пару токенов.

        Returns:
            DTO с парой токенов.

        Raises:
            InvalidRefreshTokenError: токен не найден в redis.

        """  # noqa: RUF002
        user_id = await self._token_service.get_user_id_by_refresh_token(
            refresh_token=input_dto.refresh_token,
        )
        if user_id is None:
            logger.warning(
                "auth.refresh.failed",
                reason="invalid_token",
            )
            raise InvalidRefreshTokenError

        await self._token_service.revoke_refresh_token(
            refresh_token=input_dto.refresh_token,
        )

        token_pair = await self._token_service.create_token_pair(user_id=user_id)

        logger.info("auth.refresh.success", user_id=str(user_id.value))

        return RefreshUserOutputDTO(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
