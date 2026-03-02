from mood_tracker.application.exceptions import EmailAlreadyExistsError
from mood_tracker.domain.entities import User
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.security import IPasswordHasher, ITokenService
from mood_tracker.domain.value_objects import (
    HashPassword,
    TokenPair,
    UserEmail,
    UserID,
)


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def __call__(self, email: str, password: str) -> TokenPair:
        if await self._user_repo.exists_by_email(email=UserEmail(email)):
            raise EmailAlreadyExistsError

        hash_password = self._password_hasher.hash_password(
            plain_password=password
        )
        user = User(
            id=UserID.new(),
            email=UserEmail(email),
            hash_password=HashPassword(hash_password),
        )
        await self._user_repo.save(user=user)

        return await self._token_service.generate_token_pair(user_id=user.id)
