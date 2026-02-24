from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.entities import User
from mood_tracker.domain.value_objects import UserEmail, UserName


class IUserRepository(Protocol):
    @abstractmethod
    def save(self, user: User) -> None: ...
    @abstractmethod
    def exists_by_name(self, name: UserName) -> bool: ...
    @abstractmethod
    def exists_by_email(self, email: UserEmail) -> bool: ...
