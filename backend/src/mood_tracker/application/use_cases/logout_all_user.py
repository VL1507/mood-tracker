from mood_tracker.domain.security import ITokenService


class LogoutAllUserUseCase:
    def __init__(self, token_service: ITokenService) -> None:
        self._token_service = token_service

    async def __call__(self, access_token: str) -> None:
        user_id = self._token_service.decode_access(access_token=access_token)

        await self._token_service.revoke_all_refresh(user_id=user_id)
