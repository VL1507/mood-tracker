from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from typing import Any

import jwt

from mood_tracker.config import JWT
from mood_tracker.domain.auth.repositories import ITokenRepository
from mood_tracker.domain.auth.security import ITokenService
from mood_tracker.domain.auth.value_objects import TokenPair, UserID


class TokenService(ITokenService):
    """Реализация ITokenService."""

    def __init__(self, token_repository: ITokenRepository, jwt_config: JWT) -> None:
        """Инициализация ITokenService."""
        self._token_repository = token_repository
        self._algorithm = jwt_config.ALGORITHM
        self._secret_key = jwt_config.SECRET_KEY
        self._access_exp = jwt_config.ACCESS_EXPIRE_SECONDS
        self._refresh_exp = jwt_config.REFRESH_EXPIRE_SECONDS

    async def create_token_pair(self, user_id: UserID) -> TokenPair:
        """
        Создание пары токенов.

        Returns:
            TokenPair

        """
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": str(user_id.value),
            "iat": now,
            "exp": now + timedelta(seconds=self._access_exp),
        }
        access_token = jwt.encode(  # pyright: ignore[reportUnknownMemberType]
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        refresh_token = token_urlsafe(32)

        await self._token_repository.save_refresh_token(
            user_id=user_id,
            refresh_token=refresh_token,
            ttl_seconds=self._refresh_exp,
        )

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    async def get_user_id_by_refresh_token(self, refresh_token: str) -> UserID | None:
        """
        Получение UserID по значению refresh_token.

        Returns:
            UserID | None:  None если токен не найден или истёк

        """
        return await self._token_repository.get_user_id_by_refresh_token(
            refresh_token=refresh_token,
        )

    async def revoke_refresh_token(self, refresh_token: str) -> None:
        """Отзыв refresh token."""
        await self._token_repository.delete_refresh_token(refresh_token=refresh_token)
