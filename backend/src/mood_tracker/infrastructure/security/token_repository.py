import json

from redis.asyncio.client import Redis

from mood_tracker.domain.repositories import ITokenRepository
from mood_tracker.domain.value_objects import UserID


class RedisTokenRepository(ITokenRepository):
    def __init__(self, redis: Redis[str]) -> None:
        self.redis = redis

    async def save_refresh(
        self,
        user_id: UserID,
        refresh_token: str,
        time_seconds: int,
        family_id: str,
    ) -> None:
        token_data = json.dumps(
            {
                "user_id": str(user_id.value),
                "family_id": family_id,
            }
        )

        await self.redis.setex(
            name=f"refresh:{refresh_token}",
            time=time_seconds,
            value=token_data,
        )
        await self.redis.setex(
            name=f"family:{family_id}",
            time=time_seconds,
            value=refresh_token,
        )
        await self.redis.sadd(
            f"refresh_sessions:{user_id.value}",
            family_id,
        )

    async def delete_refresh(
        self,
        refresh_token: str,
    ) -> None:
        value = await self.redis.get(name=f"refresh:{refresh_token}")
        if value is None:
            return

        data = json.loads(value)
        family_id = data["family_id"]
        user_id = data["user_id"]

        await self.redis.delete(f"refresh:{refresh_token}")
        await self.redis.delete(f"family:{family_id}")
        await self.redis.srem(
            f"refresh_sessions:{user_id}",
            family_id,
        )

    async def check_refresh(self, refresh_token: str) -> bool:
        value = await self.redis.get(name=f"refresh:{refresh_token}")
        return value is not None

    async def get_last_in_family(self, family_id: str) -> str | None:
        result = await self.redis.get(name=f"family:{family_id}")
        if result is None:
            return None
        return result

    async def get_family_by_refresh(self, refresh_token: str) -> str | None:
        value = await self.redis.get(name=f"refresh:{refresh_token}")
        if value is None:
            return None

        data: dict[str, str] = json.loads(value)

        return data.get("family_id")

    async def revoke_all_refresh(self, refresh_token: str) -> None:
        value = await self.redis.get(name=f"refresh:{refresh_token}")
        if value is None:
            return

        data = json.loads(value)
        user_id = data["user_id"]

        family_ids = await self.redis.smembers(f"refresh_sessions:{user_id}")

        for family_id in family_ids:
            refresh = await self.redis.get(f"family:{family_id}")
            if refresh:
                await self.redis.delete(f"refresh:{refresh}")

            await self.redis.delete(f"family:{family_id}")

        await self.redis.delete(f"refresh_sessions:{user_id}")
