from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.value_objects import UserID


class ITokenRepository(Protocol):
    @abstractmethod
    def save_refresh(self, user_id: UserID, refresh_token: str) -> None: ...
    @abstractmethod
    def delete_refresh(self, user_id: UserID, refresh_token: str) -> None: ...
    @abstractmethod
    def check_refresh(self, user_id: UserID, refresh_token: str) -> bool: ...
