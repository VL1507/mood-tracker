from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)
from redis.asyncio import Redis

from mood_tracker.config import Config
from mood_tracker.domain.auth.repositories import ITokenRepository
from mood_tracker.domain.auth.security import ITokenService
from mood_tracker.infrastructure.security import (
    RedisTokenRepository,
    TokenService,
)


class TokenProvider(Provider):
    """Провайдер для всего связанного с токенами."""  # noqa: RUF002

    @provide(scope=Scope.APP)
    @staticmethod
    def get_redis(config: Config) -> Redis:
        """
        Провайдер для Redis.

        Returns:
            Redis

        """
        return Redis(
            host=config.REDIS.HOST,
            port=config.REDIS.PORT,
            password=config.REDIS.PASSWORD,
            decode_responses=True,
        )

    token_repository = provide(
        RedisTokenRepository,
        scope=Scope.REQUEST,
        provides=ITokenRepository,
    )

    @provide(scope=Scope.REQUEST)
    @staticmethod
    def get_token_service(
        token_repository: ITokenRepository,
        config: Config,
    ) -> ITokenService:
        """
        Провайдер для ITokenService.

        Returns:
            TokenService: реализация ITokenService

        """
        return TokenService(token_repository=token_repository, jwt_config=config.JWT)
