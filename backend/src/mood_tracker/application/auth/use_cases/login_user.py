import structlog

from mood_tracker.application.auth.dto.login_user import (
    LoginUserInputDTO,
    LoginUserOutputDTO,
)
from mood_tracker.application.exceptions import InvalidCredentialsError
from mood_tracker.domain.auth.repositories import IUserRepository
from mood_tracker.domain.auth.security import IPasswordHasher, ITokenService
from mood_tracker.domain.auth.value_objects import UserEmail

logger = structlog.stdlib.get_logger()


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

    async def __call__(
        self, input_dto: LoginUserInputDTO
    ) -> LoginUserOutputDTO:
        """Проверяет данные пользователя и возвращает пару токенов

        Raises:
            InvalidCredentialsError: отсутствие пользователя с данной почтой
            InvalidCredentialsError: неверный пароль
        """  # noqa: RUF002
        user = await self._user_repo.get_user_by_email(
            email=UserEmail(input_dto.email)
        )
        if user is None:
            logger.warning("auth.login.failed", reason="user_not_found")
            raise InvalidCredentialsError

        if not self._password_hasher.verify_password(
            password=input_dto.password,
            password_hash=user.password_hash.value,
        ):
            logger.warning(
                "auth.login.failed",
                reason="invalid_password",
                user_id=str(user.id.value),
            )
            raise InvalidCredentialsError

        token_pair = await self._token_service.create_token_pair(
            user_id=user.id
        )

        logger.info("auth.login.success", user_id=str(user.id.value))

        return LoginUserOutputDTO(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
