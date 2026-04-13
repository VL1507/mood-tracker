from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    """Конфиг базы данных."""

    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str


class REDIS(BaseModel):
    """Конфиг redis."""

    HOST: str
    PORT: int
    PASSWORD: str


# TODO: переименовать в AUTH потому что это не только jwt
class JWT(BaseModel):
    """Конфиг jwt."""

    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_EXPIRE_SECONDS: int
    REFRESH_EXPIRE_SECONDS: int


class APP(BaseModel):
    """Конфиг приложения."""

    PORT: int
    ENV: Literal["dev", "prod"]


class Config(BaseSettings):
    """Конфиг всех конфигов."""

    DB: DB
    REDIS: REDIS
    JWT: JWT
    APP: APP

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )
