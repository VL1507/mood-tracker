from redis.asyncio.client import Redis

from mood_tracker.domain.repositories import ITokenRepository
from mood_tracker.domain.value_objects import UserID


class RedisTokenRepository(ITokenRepository):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.refresh_ttl = 30 * 24 * 60 * 60  # TODO: убрать в конфиг

    async def save_refresh(self, user_id: UserID, refresh_token: str) -> None:
        await self.redis.setex(
            name=f"refresh:{user_id.value}:{refresh_token}",
            time=self.refresh_ttl,
            value="1",
        )

    async def delete_refresh(
        self, user_id: UserID, refresh_token: str
    ) -> None:
        await self.redis.delete(f"refresh:{user_id.value}:{refresh_token}")

    async def check_refresh(self, user_id: UserID, refresh_token: str) -> bool:
        value = await self.redis.get(
            name=f"refresh:{user_id.value}:{refresh_token}"
        )
        return value is not None
