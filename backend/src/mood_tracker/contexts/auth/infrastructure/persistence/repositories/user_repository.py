from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mood_tracker.contexts.auth.domain.entities import User
from mood_tracker.contexts.auth.domain.repositories import IUserRepository
from mood_tracker.contexts.auth.domain.value_objects import (
    PasswordHash,
    UserEmail,
    UserID,
)
from mood_tracker.contexts.auth.infrastructure.persistence.models import UserORM


class UserRepository(IUserRepository):
    """Реализация IUserRepository на SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация UserRepository."""
        self._session = session

    async def save(self, user: User) -> None:
        """Сохранение User."""
        user_orm = self._domain_to_orm(user_domain=user)
        self._session.add(user_orm)
        await self._session.commit()

    async def user_exists_by_email(self, email: UserEmail) -> bool:
        """
        Проверка существования User по UserEmail.

        Returns:
            bool: True если существует, False иначе

        """
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_user_by_email(self, email: UserEmail) -> User | None:
        """
        Получение User по UserEmail.

        Returns:
            User | None: None если пользователь не найден.

        """
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        user_orm = result.scalar()
        if user_orm is None:
            return None
        return self._orm_to_domain(user_orm=user_orm)

    @staticmethod
    def _domain_to_orm(user_domain: User) -> UserORM:
        user_orm = UserORM()
        user_orm.id = user_domain.id.value
        user_orm.email = user_domain.email.value
        user_orm.password_hash = user_domain.password_hash.value
        return user_orm

    @staticmethod
    def _orm_to_domain(user_orm: UserORM) -> User:
        return User(
            id=UserID(user_orm.id),
            email=UserEmail(user_orm.email),
            password_hash=PasswordHash(user_orm.password_hash),
        )
