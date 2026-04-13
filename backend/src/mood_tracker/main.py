import uvicorn

from mood_tracker.config import Config
from mood_tracker.logging import setup_logging


def main() -> None:
    """Запуск FastAPI приложения в помощью uvicorn."""
    config = Config()  # pyright: ignore[reportCallIssue] # ty:ignore[missing-argument]
    setup_logging(env=config.APP.ENV)

    uvicorn.run(
        "mood_tracker.app_factory:create_app",
        factory=True,
        host="0.0.0.0",  # noqa: S104
        port=config.APP.PORT,
        log_config=None,
        access_log=config.APP.ENV == "dev",
    )


if __name__ == "__main__":
    main()
