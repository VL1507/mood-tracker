from pydantic import BaseModel, EmailStr


class UserLoginRequest(BaseModel):
    """Схема данных запроса для входа в аккаунт."""

    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    """Схема данных ответа для входа в аккаунт."""

    access_token: str
