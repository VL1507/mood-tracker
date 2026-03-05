from dishka import Provider, Scope, provide

from mood_tracker.config import Config
from mood_tracker.presentation.api.cookie_service import CookieService


class CookieServiceProvider(Provider):
    @provide(scope=Scope.APP)
    @staticmethod
    def get_cookie_service(config: Config) -> CookieService:
        return CookieService(config=config)
