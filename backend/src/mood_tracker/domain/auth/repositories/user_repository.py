from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.auth.entities import User
from mood_tracker.domain.auth.value_objects import UserEmail


class IUserRepository(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def user_exists_by_email(self, email: UserEmail) -> bool: ...

    @abstractmethod
    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """None если пользователь не найден."""
        ...
