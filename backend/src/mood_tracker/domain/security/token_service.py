from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.value_objects import TokenPair, UserID


class ITokenService(Protocol):
    @abstractmethod
    async def create_session(self, user_id: UserID) -> TokenPair: ...
