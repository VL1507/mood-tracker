import json
from typing import TYPE_CHECKING, cast

from redis.asyncio.client import Redis

from mood_tracker.domain.repositories import ITokenRepository
from mood_tracker.domain.value_objects import UserID

if TYPE_CHECKING:
    from collections.abc import Awaitable


class RedisTokenRepository(ITokenRepository):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def save_refresh(
        self,
        user_id: UserID,
        refresh_token: str,
        time_seconds: int,
    ) -> None:
        token_data = json.dumps(
            {
                "user_id": str(user_id.value),
            }
        )

        await self.redis.setex(
            name=f"refresh:{refresh_token}",
            time=time_seconds,
            value=token_data,
        )

        await cast(
            "Awaitable[int]",
            self.redis.sadd(
                f"refresh_sessions:{user_id.value}",
                refresh_token,
            ),
        )

    async def delete_refresh(
        self,
        refresh_token: str,
    ) -> None:
        value = await self.redis.get(name=f"refresh:{refresh_token}")
        value = cast("str | None", value)
        if value is None:
            return

        data: dict[str, str] = json.loads(value)
        user_id = data["user_id"]

        await self.redis.delete(f"refresh:{refresh_token}")
        await cast(
            "Awaitable[int]",
            self.redis.srem(
                f"refresh_sessions:{user_id}",
                refresh_token,
            ),
        )

    async def check_refresh(self, refresh_token: str) -> bool:
        value = await self.redis.get(name=f"refresh:{refresh_token}")
        value = cast("str | None", value)
        return value is not None

    async def revoke_all_refresh(self, user_id: UserID) -> None:
        refresh_tokens = await cast(
            "Awaitable[set[str]]",
            self.redis.smembers(f"refresh_sessions:{user_id.value}"),
        )
        for refresh_token in refresh_tokens:
            await self.redis.delete(f"refresh:{refresh_token}")
            await self.redis.srem(
                f"refresh_sessions:{user_id.value}", refresh_token
            )
