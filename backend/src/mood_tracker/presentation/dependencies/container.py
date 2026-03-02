from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from mood_tracker.config import Config


def make_container_di(config: Config) -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        context={Config: config},
    )
