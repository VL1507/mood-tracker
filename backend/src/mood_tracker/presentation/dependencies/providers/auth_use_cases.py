from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from mood_tracker.application.auth.use_cases import (
    LoginUserUseCase,
    RefreshUserUseCase,
    RegisterUserUseCase,
)


class AuthUseCasesProvider(Provider):
    scope = Scope.REQUEST

    register_user = provide(RegisterUserUseCase)
    login_user = provide(LoginUserUseCase)
    refresh_user = provide(RefreshUserUseCase)
