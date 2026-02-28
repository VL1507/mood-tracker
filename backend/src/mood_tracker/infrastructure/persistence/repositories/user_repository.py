from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mood_tracker.domain.entities import User
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.value_objects import HashPassword, UserEmail, UserID
from mood_tracker.infrastructure.persistence.models import UserORM


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, user: User) -> None:
        user_orm = self._domain_to_orm(user_domain=user)
        self.session.add(user_orm)
        await self.session.commit()

    async def exists_by_email(self, email: UserEmail) -> bool:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_by_email(self, email: UserEmail) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self.session.execute(stmt)
        user_orm = result.scalar()
        if user_orm is None:
            return None
        return self._orm_to_domain(user_orm=user_orm)

    @staticmethod
    def _domain_to_orm(user_domain: User) -> UserORM:
        user_orm = UserORM()
        user_orm.id = user_domain.id.value
        user_orm.email = user_domain.email.value
        user_orm.hash_password = user_domain.hash_password.value
        return user_orm

    @staticmethod
    def _orm_to_domain(user_orm: UserORM) -> User:
        return User(
            id=UserID(user_orm.id),
            email=UserEmail(user_orm.email),
            hash_password=HashPassword(user_orm.hash_password),
        )
