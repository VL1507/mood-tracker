from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from mood_tracker.domain.value_objects import UserID


class ITokenRepository(Protocol):
    @abstractmethod
    async def save_refresh(
        self,
        user_id: UserID,
        refresh_token: UUID,
        time_seconds: int,
    ) -> None: ...
