from abc import abstractmethod
from typing import Literal, Protocol

from mood_tracker.domain.value_objects import TokenPair, UserID


class ITokenService(Protocol):
    @abstractmethod
    async def generate_token_pair(self, user_id: UserID) -> TokenPair: ...
    @abstractmethod
    def decode_access(self, access_token: str) -> UserID: ...
    @abstractmethod
    async def verify_refresh(self, refresh_token: str) -> bool: ...
    @abstractmethod
    async def revoke_refresh(self, refresh_token: str) -> None: ...
    @abstractmethod
    async def revoke_all_refresh(self, user_id: UserID) -> None: ...
    @abstractmethod
    async def get_user_id_by_refresh(
        self, refresh_token: str
    ) -> UserID | None: ...
