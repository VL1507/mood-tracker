from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from mood_tracker.domain.auth.security import IPasswordHasher
from mood_tracker.infrastructure.security import PasswordHasher


class PasswordHasherProvider(Provider):
    """Провайдер для PasswordHasher."""

    password_hasher = provide(
        PasswordHasher,
        scope=Scope.APP,
        provides=IPasswordHasher,
    )
