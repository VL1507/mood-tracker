from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from mood_tracker.presentation.api.cookie_service import CookieService


class CookieServiceProvider(Provider):
    cookie_service = provide(CookieService, scope=Scope.APP)
