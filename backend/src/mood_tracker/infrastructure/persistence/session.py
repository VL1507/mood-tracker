from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from mood_tracker.config import DB


def new_async_session_maker(
    db_config: DB,
) -> async_sessionmaker[AsyncSession]:
    """
    Создание async_sessionmaker[AsyncSession].

    Returns:
        async_sessionmaker[AsyncSession]

    """
    url = URL.create(
        drivername="postgresql+psycopg",
        username=db_config.USER,
        password=db_config.PASSWORD,
        host=db_config.HOST,
        port=db_config.PORT,
        database=db_config.NAME,
    )
    engine = create_async_engine(
        url=url,
    )
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
