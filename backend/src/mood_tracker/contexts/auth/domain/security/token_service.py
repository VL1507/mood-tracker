from abc import abstractmethod
from typing import Protocol

from mood_tracker.contexts.auth.domain.value_objects import TokenPair
from mood_tracker.shared.domain.value_objects import UserID


class ITokenService(Protocol):
    """Сервис работы с токенами access и refresh."""  # noqa: RUF002

    @abstractmethod
    async def create_token_pair(self, user_id: UserID) -> TokenPair:
        """Создание пары токенов."""

    @abstractmethod
    async def get_user_id_by_refresh_token(self, refresh_token: str) -> UserID | None:
        """
        Получение UserID по значению refresh_token.

        None если токен не найден или истёк.
        """

    @abstractmethod
    async def revoke_refresh_token(self, refresh_token: str) -> None:
        """Отзыв refresh token."""
