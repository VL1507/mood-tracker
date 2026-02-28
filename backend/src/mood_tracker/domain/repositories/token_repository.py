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
        family_id: str,
    ) -> None: ...
    @abstractmethod
    async def delete_refresh(
        self,
        refresh_token: str,
    ) -> None: ...
    @abstractmethod
    async def check_refresh(self, refresh_token: str) -> bool: ...
    @abstractmethod
    async def get_last_in_family(self, family_id: str) -> str | None: ...
    @abstractmethod
    async def get_family_by_refresh(
        self, refresh_token: str
    ) -> str | None: ...
    @abstractmethod
    async def revoke_all_refresh(self, refresh_token: str) -> None: ...
