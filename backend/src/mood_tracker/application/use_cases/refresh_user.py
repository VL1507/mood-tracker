from mood_tracker.application.dto.refresh_user import (
    RefreshUserInputDTO,
    RefreshUserOutputDTO,
)
from mood_tracker.application.exceptions import InvalidRefreshTokenError
from mood_tracker.domain.security import ITokenService


class RefreshUserUseCase:
    def __init__(self, token_service: ITokenService) -> None:
        self._token_service = token_service

    async def __call__(
        self, input_dto: RefreshUserInputDTO
    ) -> RefreshUserOutputDTO:
        """Принимает старый refresh token и возвращает новую пару токенов

        Raises:
            InvalidRefreshTokenError: токен не найден в redis
        """
        user_id = await self._token_service.get_user_id_by_refresh_token(
            refresh_token=input_dto.refresh_token
        )
        if user_id is None:
            raise InvalidRefreshTokenError

        await self._token_service.revoke_refresh_token(
            refresh_token=input_dto.refresh_token
        )

        token_pair = await self._token_service.create_token_pair(
            user_id=user_id
        )

        return RefreshUserOutputDTO(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
