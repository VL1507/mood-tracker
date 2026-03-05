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
