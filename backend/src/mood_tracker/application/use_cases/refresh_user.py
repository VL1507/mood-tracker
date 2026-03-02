from mood_tracker.domain.security import ITokenService
from mood_tracker.domain.value_objects import TokenPair


class RefreshUserUseCase:
    def __init__(self, token_service: ITokenService) -> None:
        self.token_service = token_service

    async def __call__(self, refresh_token: str) -> TokenPair:
        user_id = await self.token_service.get_user_id_by_refresh(
            refresh_token=refresh_token
        )

        if user_id is None:
            raise ValueError("неверный refresh")

        await self.token_service.revoke_refresh(refresh_token=refresh_token)

        return await self.token_service.generate_token_pair(user_id=user_id)
