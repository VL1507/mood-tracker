from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from mood_tracker.config import Config
from mood_tracker.domain.repositories import ITokenRepository
from mood_tracker.infrastructure.security import RedisTokenRepository


class TokenProvider(Provider):
    @provide(scope=Scope.APP)
    @staticmethod
    def get_redis(config: Config) -> Redis:
        return Redis(
            host=config.REDIS.HOST,
            port=config.REDIS.PORT,
            password=config.REDIS.PASSWORD,
        )

    @provide(scope=Scope.REQUEST)
    @staticmethod
    def get_token_repository(redis: Redis) -> ITokenRepository:
        return RedisTokenRepository(redis=redis)
