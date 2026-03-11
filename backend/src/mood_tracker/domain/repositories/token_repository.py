from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.value_objects import UserID


class ITokenRepository(Protocol):
    @abstractmethod
    async def save_refresh_token(
        self,
        user_id: UserID,
        refresh_token: str,
        time_seconds: int,
    ) -> None: ...
    @abstractmethod
    async def get_user_id_by_refresh_token(
        self, refresh_token: str
    ) -> UserID | None: ...
    @abstractmethod
    async def delete_refresh_token(
        self,
        refresh_token: str,
    ) -> None: ...
