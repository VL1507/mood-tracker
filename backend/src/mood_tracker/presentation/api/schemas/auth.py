import re

from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")  # TODO: возможно стоит переделать ошибки
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )
        if not any(c.islower() for c in v):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError(
                "Password must contain at least one special character (!@#$%^&*)"
            )
        return v


class UserRegisterResponse(BaseModel):
    access_token: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
