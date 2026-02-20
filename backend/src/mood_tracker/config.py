from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class REDIS(BaseModel):
    HOST: str
    PORT: int
    PASSWORD: str


class DB(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str


class Config(BaseSettings):
    DB: DB
    REDIS: REDIS

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )
