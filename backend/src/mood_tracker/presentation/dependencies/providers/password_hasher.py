from dishka import Provider, Scope, provide

from mood_tracker.domain.security import IPasswordHasher
from mood_tracker.infrastructure.security import Argon2PasswordHasher


class PasswordHasherProvider(Provider):
    @provide(scope=Scope.APP)
    @staticmethod
    def get_session_maker() -> IPasswordHasher:
        return Argon2PasswordHasher()
