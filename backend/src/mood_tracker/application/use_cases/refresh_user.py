from mood_tracker.application.exceptions import InvalidRefreshTokenError
from mood_tracker.domain.security import ITokenService
from mood_tracker.domain.value_objects import TokenPair


class RefreshUserUseCase:
    def __init__(self, token_service: ITokenService) -> None:
        self._token_service = token_service

    async def __call__(self, refresh_token: str) -> TokenPair:
        user_id = await self._token_service.get_user_id_by_refresh(
            refresh_token=refresh_token
        )
        if user_id is None:
            raise InvalidRefreshTokenError

        await self._token_service.revoke_refresh(refresh_token=refresh_token)

        return await self._token_service.generate_token_pair(user_id=user_id)
