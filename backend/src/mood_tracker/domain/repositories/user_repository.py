from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.entities import User
from mood_tracker.domain.value_objects import UserEmail


class IUserRepository(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None: ...
    @abstractmethod
    async def exists_by_email(self, email: UserEmail) -> bool: ...
