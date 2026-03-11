from mood_tracker.application.dto.login_user import (
    LoginUserInputDTO,
    LoginUserOutputDTO,
)
from mood_tracker.application.exceptions import InvalidCredentialsError
from mood_tracker.domain.repositories import IUserRepository
from mood_tracker.domain.security import IPasswordHasher, ITokenService
from mood_tracker.domain.value_objects import UserEmail


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
        """Проверяет пользователя по почте и паролю, создает и возвращает новую
        пару токенов

        Args:
            input_dto (LoginUserInputDTO): dto содержащие почту и пароль
            пользователя

        Raises:
            InvalidCredentialsError: отсутствие пользователя с данной почтой
            InvalidCredentialsError: неверный пароль

        Returns:
            LoginUserOutputDTO: содержит новые access_token и refresh_token
        """  # noqa: RUF002
        user = await self._user_repo.get_user_by_email(
            email=UserEmail(input_dto.email)
        )
        if user is None:
            raise InvalidCredentialsError

        if not self._password_hasher.verify_password(
            password=input_dto.password,
            password_hash=user.password_hash.value,
        ):
            raise InvalidCredentialsError

        token_pair = await self._token_service.create_token_pair(
            user_id=user.id
        )

        return LoginUserOutputDTO(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
        )
