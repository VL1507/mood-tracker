from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from mood_tracker.config import DB


def new_async_session_maker(
    db_config: DB,
) -> async_sessionmaker[AsyncSession]:
    database_uri = f"postgresql+psycopg://{db_config.USER}:{db_config.PASSWORD}@{db_config.HOST}:{db_config.PORT}/{db_config.NAME}"

    engine = create_async_engine(
        url=database_uri,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
