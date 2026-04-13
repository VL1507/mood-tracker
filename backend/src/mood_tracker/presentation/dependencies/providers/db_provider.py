from collections.abc import AsyncIterable

from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from mood_tracker.config import Config
from mood_tracker.domain.auth.repositories.user_repository import (
    IUserRepository,
)
from mood_tracker.infrastructure.persistence.repositories import (
    UserRepository,
)
from mood_tracker.infrastructure.persistence.session import (
    new_async_session_maker,
)


class DBProvider(Provider):
    """Провайдер для всего связанного с БД."""  # noqa: RUF002

    @provide(scope=Scope.APP)
    @staticmethod
    def get_session_maker(config: Config) -> async_sessionmaker[AsyncSession]:
        """
        Провайдер для async_sessionmaker[AsyncSession].

        Returns:
            async_sessionmaker[AsyncSession]

        """
        return new_async_session_maker(db_config=config.DB)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_session(
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        """
        Провайдер сессии.

        Yields:
            Iterator[AsyncIterable[AsyncSession]]

        """
        async with session_maker() as session:
            yield session

    user_repository = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=IUserRepository,
    )
