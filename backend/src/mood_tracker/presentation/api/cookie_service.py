from dataclasses import dataclass
from typing import Literal

from fastapi import Response

from mood_tracker.config import Config
from mood_tracker.constants import REFRESH_TOKEN_COOKIE_NAME


@dataclass(frozen=True)
class RefreshCookieConfig:
    key: str
    max_age: int
    secure: bool
    httponly: bool = True
    samesite: Literal["lax", "strict", "none"] | None = "lax"
    path: str = "/api/auth"


class CookieService:
    def __init__(self, config: Config) -> None:
        self._refresh_config = RefreshCookieConfig(
            key=REFRESH_TOKEN_COOKIE_NAME,
            max_age=config.JWT.REFRESH_EXPIRE_SECONDS,
            secure=True,
        )

    def set_refresh_token(self, response: Response, token: str) -> None:
        response.set_cookie(
            key=self._refresh_config.key,
            value=token,
            max_age=self._refresh_config.max_age,
            secure=self._refresh_config.secure,
            httponly=self._refresh_config.httponly,
            samesite=self._refresh_config.samesite,
            path=self._refresh_config.path,
        )

    def delete_refresh_token(self, response: Response) -> None:
        response.delete_cookie(
            key=self._refresh_config.key,
            path=self._refresh_config.path,
        )
