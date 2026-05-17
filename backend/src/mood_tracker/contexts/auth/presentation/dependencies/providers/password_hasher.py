from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from mood_tracker.contexts.auth.domain.security import IPasswordHasher
from mood_tracker.contexts.auth.infrastructure.security import PasswordHasher


class PasswordHasherProvider(Provider):
    """Провайдер для PasswordHasher."""

    password_hasher = provide(
        PasswordHasher,
        scope=Scope.APP,
        provides=IPasswordHasher,
    )
