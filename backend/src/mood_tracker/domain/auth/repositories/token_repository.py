from abc import abstractmethod
from typing import Protocol

from mood_tracker.domain.auth.value_objects import UserID


class ITokenRepository(Protocol):
    """Репозиторий для работы с refresh токенами."""  # noqa: RUF002

    @abstractmethod
    async def save_refresh_token(
        self,
        user_id: UserID,
        refresh_token: str,
        ttl_seconds: int,
    ) -> None:
        """Сохранения refresh token."""

    @abstractmethod
    async def get_user_id_by_refresh_token(self, refresh_token: str) -> UserID | None:
        """
        Получение UserID по значению refresh token.

        None если токен не найден или истёк.
        """

    @abstractmethod
    async def delete_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        """Удаление refresh token."""
