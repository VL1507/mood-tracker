from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DB(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str


class REDIS(BaseModel):
    HOST: str
    PORT: int
    PASSWORD: str


class JWT(BaseModel):
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_EXPIRE_SECONDS: int
    REFRESH_EXPIRE_SECONDS: int


class Config(BaseSettings):
    DB: DB
    REDIS: REDIS
    JWT: JWT

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )
