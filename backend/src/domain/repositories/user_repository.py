from abc import abstractmethod
from typing import Protocol

from src.domain.entities.user import User


class IUserRepository(Protocol):
    @abstractmethod
    def save(self, user: User) -> None:
        pass
