from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from mood_tracker.application.exceptions import EmailAlreadyExistsError


def email_already_exists_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,  # noqa: ARG001
) -> JSONResponse:
    return JSONResponse(
        content={"detail": "A user with this email is already registered"},
        status_code=status.HTTP_409_CONFLICT,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        EmailAlreadyExistsError, email_already_exists_handler
    )
