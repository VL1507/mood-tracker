from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.value_objects import TokenPair, UserID


class ITokenService(Protocol):
    @abstractmethod
    async def generate_token_pair(self, user_id: UserID) -> TokenPair: ...
    @abstractmethod
    def verify_access(self, access_token: str) -> bool: ...
    @abstractmethod
    def decode_access(self, access_token: str) -> UserID | None: ...
    @abstractmethod
    async def verify_refresh(
        self, user_id: UserID, refresh_token: str
    ) -> bool: ...
    @abstractmethod
    async def revoke_refresh(
        self, user_id: UserID, refresh_token: str
    ) -> None: ...
