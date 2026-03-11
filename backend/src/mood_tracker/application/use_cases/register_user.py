from mood_tracker.application.dto.register_user import (
    RegisterUserInputDTO,
    RegisterUserOutputDTO,
)
from mood_tracker.application.exceptions import EmailAlreadyExistsError
from mood_tracker.domain.entities import User
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.security import IPasswordHasher, ITokenService
from mood_tracker.domain.value_objects import (
    PasswordHash,
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

    async def __call__(
        self, input_dto: RegisterUserInputDTO
    ) -> RegisterUserOutputDTO:
        if await self._user_repo.exists_by_email(
            email=UserEmail(input_dto.email)
        ):
            raise EmailAlreadyExistsError

        password_hash = self._password_hasher.hash_password(
            password=input_dto.password
        )
        user = User(
            id=UserID.new(),
            email=UserEmail(input_dto.email),
            password_hash=PasswordHash(password_hash),
        )
        await self._user_repo.save(user=user)

        token_pair = await self._token_service.create_token_pair(
            user_id=user.id
        )

        return RegisterUserOutputDTO(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
