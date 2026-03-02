from dataclasses import dataclass

from fastapi import Response

from mood_tracker.config import Config


@dataclass(frozen=True)
class CookieConfig:
    key: str
    max_age: int
    secure: bool
    httponly: bool = True
    samesite: str = "lax"  # TODO: возможно стоит изменить
    path: str = "/api/auth"


class CookieService:
    def __init__(self, config: Config) -> None:
        self._refresh_config = CookieConfig(
            key="refresh_token",
            max_age=config.JWT.REFRESH_EXPIRE_SECONDS,
            secure=False,  # TODO: брать из конфига
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
