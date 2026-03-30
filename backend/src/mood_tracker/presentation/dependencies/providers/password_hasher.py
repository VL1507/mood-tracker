from dishka import Provider, Scope, provide

from mood_tracker.domain.security import IPasswordHasher
from mood_tracker.infrastructure.security import PasswordHasher


class PasswordHasherProvider(Provider):
    password_hasher = provide(
        PasswordHasher,
        scope=Scope.APP,
        provides=IPasswordHasher,
    )
