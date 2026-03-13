from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.entities import User
from mood_tracker.domain.value_objects import UserEmail


class IUserRepository(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None:
        """Сохраняет пользователя

        Args:
            user (User): доменная модель пользователя
        """
        ...

    @abstractmethod
    async def exists_by_email(self, email: UserEmail) -> bool:
        """Проверяет существует ло пользователь с данной почтой

        Args:
            email (UserEmail): доменная модель почты пользователя

        Returns:
            bool: True - если был найден, иначе False
        """  # noqa: RUF002
        ...

    @abstractmethod
    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """Получает пользователя по значению почты. Если не находит, то
        возвращает None

        Args:
            email (UserEmail): доменная модель почты пользователя

        Returns:
            User | None
        """
        ...
