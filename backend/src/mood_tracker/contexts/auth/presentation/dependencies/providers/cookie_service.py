from dishka import (
    Provider,
    Scope,
    provide,  # pyright: ignore[reportUnknownVariableType]
)

from mood_tracker.contexts.auth.presentation.api.cookie_service import CookieService


class CookieServiceProvider(Provider):
    """Провайдер для CookieService."""

    cookie_service = provide(CookieService, scope=Scope.APP)
