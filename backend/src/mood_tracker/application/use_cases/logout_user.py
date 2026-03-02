from mood_tracker.domain.security import ITokenService


class LogoutUserUseCase:
    def __init__(self, token_service: ITokenService) -> None:
        self._token_service = token_service

    async def __call__(self, refresh_token: str) -> None:
        await self._token_service.revoke_refresh(refresh_token=refresh_token)
