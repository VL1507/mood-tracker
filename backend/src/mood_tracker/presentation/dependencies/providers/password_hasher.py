from dishka import Provider, Scope, provide

from mood_tracker.domain.security import IPasswordHasher
from mood_tracker.infrastructure.security import PasswordHasher


class PasswordHasherProvider(Provider):
    @provide(scope=Scope.APP)
    @staticmethod
    def get_session_maker() -> IPasswordHasher:
        return PasswordHasher()
