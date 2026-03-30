import structlog

from mood_tracker.application.auth.dto.register_user import (
    RegisterUserInputDTO,
    RegisterUserOutputDTO,
)
from mood_tracker.application.exceptions import EmailAlreadyExistsError
from mood_tracker.domain.auth.entities import User
from mood_tracker.domain.auth.repositories import IUserRepository
from mood_tracker.domain.auth.security import IPasswordHasher, ITokenService
from mood_tracker.domain.auth.value_objects import (
    PasswordHash,
    UserEmail,
    UserID,
)

logger = structlog.stdlib.get_logger()


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

    async def __call__(self, input_dto: RegisterUserInputDTO) -> RegisterUserOutputDTO:
        """Регистрирует нового пользователя и возвращает пару токенов.

        Raises:
            EmailAlreadyExistsError: пользователь с данным email уже существует.

        Returns:
            DTO с парой токенов.
        """  # noqa: RUF002
        if await self._user_repo.user_exists_by_email(email=UserEmail(input_dto.email)):
            # TODO: возможно стоит искать юзера по email
            # и возвращать его id в лог  # noqa: RUF003
            logger.warning("auth.register.failed", reason="email_already_exists")
            raise EmailAlreadyExistsError

        password_hash = self._password_hasher.hash_password(password=input_dto.password)
        user = User(
            id=UserID.new(),
            email=UserEmail(input_dto.email),
            password_hash=PasswordHash(password_hash),
        )
        await self._user_repo.save(user=user)

        token_pair = await self._token_service.create_token_pair(user_id=user.id)

        logger.info("auth.register.success", user_id=str(user.id.value))

        return RegisterUserOutputDTO(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
