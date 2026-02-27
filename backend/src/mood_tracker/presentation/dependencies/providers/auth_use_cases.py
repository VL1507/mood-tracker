from dishka import Provider, Scope, provide

from mood_tracker.application.use_cases import RegisterUserUseCase
from mood_tracker.domain.repositories.user_repository import IUserRepository
from mood_tracker.domain.security.password_hasher import IPasswordHasher
from mood_tracker.domain.security.token_service import ITokenService


class AuthUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    @staticmethod
    def get_register_user_use_case(
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repo=user_repo,
            password_hasher=password_hasher,
            token_service=token_service,
        )
