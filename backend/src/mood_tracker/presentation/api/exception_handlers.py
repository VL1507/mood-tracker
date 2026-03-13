from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from mood_tracker.application.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)


def email_already_exists_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    return JSONResponse(
        content={"detail": "A user with this email is already registered"},
        status_code=status.HTTP_409_CONFLICT,
    )


def invalid_credentials_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    return JSONResponse(
        content={"detail": "Invalid login or password"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def invalid_refresh_token_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    return JSONResponse(
        content={"detail": "Invalid refresh token"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        EmailAlreadyExistsError, email_already_exists_handler
    )
    app.add_exception_handler(
        InvalidCredentialsError, invalid_credentials_handler
    )
    app.add_exception_handler(
        InvalidRefreshTokenError, invalid_refresh_token_handler
    )
