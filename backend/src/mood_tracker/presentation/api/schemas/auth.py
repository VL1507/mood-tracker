import re

from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")  # TODO: возможно стоит переделать ошибки
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters long")
        if not any(c.isupper() for c in password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )
        if not any(c.islower() for c in password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*]", password):
            raise ValueError(
                "Password must contain at least one special character (!@#$%^&*)"
            )
        return password


class UserRegisterResponse(BaseModel):
    access_token: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str


class UserRefreshResponse(BaseModel):
    access_token: str
