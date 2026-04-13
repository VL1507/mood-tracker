from pydantic import BaseModel


class UserRefreshResponse(BaseModel):
    """Схема данных ответа для обновления токенов."""

    access_token: str
