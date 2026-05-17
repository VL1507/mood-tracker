from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from mood_tracker.config import Config

from .providers import (
    AuthUseCasesProvider,
    CookieServiceProvider,
    DBProvider,
    PasswordHasherProvider,
    TokenProvider,
)


def make_container_di(config: Config) -> AsyncContainer:
    """
    Создание асинхронного контейнера.

    Returns:
        AsyncContainer

    """
    return make_async_container(
        AuthUseCasesProvider(),
        CookieServiceProvider(),
        DBProvider(),
        PasswordHasherProvider(),
        TokenProvider(),
        FastapiProvider(),
        context={Config: config},
    )
