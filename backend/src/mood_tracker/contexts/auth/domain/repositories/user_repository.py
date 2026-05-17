from abc import abstractmethod
from typing import Protocol

from mood_tracker.contexts.auth.domain.entities import User
from mood_tracker.contexts.auth.domain.value_objects import UserEmail


class IUserRepository(Protocol):
    """Протокол User репозитория."""

    @abstractmethod
    async def save(self, user: User) -> None:
        """Сохранение User."""

    @abstractmethod
    async def user_exists_by_email(self, email: UserEmail) -> bool:
        """Проверка существования User по UserEmail."""

    @abstractmethod
    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """
        Получение User по UserEmail.

        None если пользователь не найден.
        """
        ...
