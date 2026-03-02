from mood_tracker.application.exceptions import InvalidCredentialsError
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.security import IPasswordHasher, ITokenService
from mood_tracker.domain.value_objects import (
    TokenPair,
    UserEmail,
)


class LoginUserUseCase:
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
        user = await self._user_repo.get_by_email(email=UserEmail(email))
        if user is None:
            raise InvalidCredentialsError

        if not self._password_hasher.verify_password(
            plain_password=password, hashed_password=user.hash_password.value
        ):
            raise InvalidCredentialsError

        return await self._token_service.generate_token_pair(user_id=user.id)
