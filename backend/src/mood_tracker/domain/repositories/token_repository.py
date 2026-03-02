from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.value_objects import UserID


class ITokenRepository(Protocol):
    @abstractmethod
    async def save_refresh(
        self,
        user_id: UserID,
        refresh_token: str,
        time_seconds: int,
    ) -> None: ...
    @abstractmethod
    async def delete_refresh(
        self,
        refresh_token: str,
    ) -> None: ...
    @abstractmethod
    async def check_refresh(self, refresh_token: str) -> bool: ...
    @abstractmethod
    async def revoke_all_refresh(self, user_id: UserID) -> None: ...
