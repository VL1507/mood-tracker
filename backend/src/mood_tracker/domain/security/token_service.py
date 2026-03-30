from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.value_objects import TokenPair, UserID


class ITokenService(Protocol):
    @abstractmethod
    async def create_token_pair(self, user_id: UserID) -> TokenPair: ...
    @abstractmethod
    async def get_user_id_by_refresh_token(
        self, refresh_token: str
    ) -> UserID | None:
        """None если токен не найден или истёк."""
        ...

    @abstractmethod
    async def revoke_refresh_token(self, refresh_token: str) -> None: ...
