from mood_tracker.application.dto.register_user import RegisterUserInputDTO
from mood_tracker.application.exceptions import EmailAlreadyExistsError
from mood_tracker.domain.entities import User
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.security import IPasswordHasher, ITokenService
from mood_tracker.domain.value_objects import (
    PasswordHash,
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

    async def __call__(self, context: RegisterUserInputDTO) -> TokenPair:
        if await self._user_repo.exists_by_email(
            email=UserEmail(context.email)
        ):
            raise EmailAlreadyExistsError

        password_hash = self._password_hasher.hash_password(
            password=context.password
        )
        user = User(
            id=UserID.new(),
            email=UserEmail(context.email),
            password_hash=PasswordHash(password_hash),
        )
        await self._user_repo.save(user=user)

        return await self._token_service.create_session(user_id=user.id)
