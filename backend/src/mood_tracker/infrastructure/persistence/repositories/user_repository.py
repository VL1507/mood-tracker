from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mood_tracker.domain.entities import User
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.value_objects import PasswordHash, UserEmail, UserID
from mood_tracker.infrastructure.persistence.models import UserORM


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        user_orm = self._domain_to_orm(user_domain=user)
        self._session.add(user_orm)
        await self._session.commit()

    async def exists_by_email(self, email: UserEmail) -> bool:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

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
