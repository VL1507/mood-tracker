import json
from typing import TYPE_CHECKING, cast

from redis.asyncio.client import Redis

from mood_tracker.domain.auth.repositories import ITokenRepository
from mood_tracker.domain.auth.value_objects import UserID

if TYPE_CHECKING:
    from collections.abc import Awaitable


class RedisTokenRepository(ITokenRepository):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def save_refresh_token(
        self,
        user_id: UserID,
        refresh_token: str,
        ttl_seconds: int,
    ) -> None:
        token_data = json.dumps(
            {
                "user_id": str(user_id.value),
            }
        )

        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.setex(
                name=f"refresh:{refresh_token}",
                time=ttl_seconds,
                value=token_data,
            )
            await cast(
                "Awaitable[int]",
                pipe.sadd(f"refresh_sessions:{user_id.value}", refresh_token),
            )
            await pipe.execute()

    async def get_user_id_by_refresh_token(self, refresh_token: str) -> UserID | None:
        value = await self._redis.get(name=f"refresh:{refresh_token}")
        value = cast("str | None", value)
        if value is None:
            return None

        data: dict[str, str] = json.loads(value)
        user_id_str = data["user_id"]
        return UserID.from_str(user_id_str)

    async def delete_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        user_id = await self.get_user_id_by_refresh_token(refresh_token=refresh_token)
        if user_id is None:
            return

        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.delete(f"refresh:{refresh_token}")
            await cast(
                "Awaitable[int]",
                pipe.srem(
                    f"refresh_sessions:{user_id.value}",
                    refresh_token,
                ),
            )
            await pipe.execute()
