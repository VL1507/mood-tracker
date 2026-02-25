from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from mood_tracker.config import Config


class RedisProvider(Provider):

    @provide(scope=Scope.APP)
    @staticmethod
    def get_redis(config: Config) -> Redis:
        return Redis(
            host=config.REDIS.HOST,
            port=config.REDIS.PORT,
            password=config.REDIS.PASSWORD,
        )
