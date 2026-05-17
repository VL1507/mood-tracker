import re

from pydantic import BaseModel, EmailStr, field_validator

MIN_PASSWORD_LEN = 12


class UserRegisterRequest(BaseModel):
    """Схема данных запроса для регистрации."""

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """
        Валидация пароля.

        Args:
            password (str): пароль

        Returns:
            str: пароль без изменения

        Raises:
            ValueError: Ошибка в длине пароля
            ValueError: Пароль без букв верхнего регистра
            ValueError: Пароль без букв нижнего регистра
            ValueError: Пароль без цифр
            ValueError: Пароль без специальных символов

        """
        if len(password) < MIN_PASSWORD_LEN:
            msg = "Password must be at least 12 characters long"
            raise ValueError(msg)
        if not any(c.isupper() for c in password):
            msg = "Password must contain at least one uppercase letter"
            raise ValueError(msg)
        if not any(c.islower() for c in password):
            msg = "Password must contain at least one lowercase letter"
            raise ValueError(msg)
        if not any(c.isdigit() for c in password):
            msg = "Password must contain at least one digit"
            raise ValueError(msg)
        if not re.search(r"[!@#$%^&*]", password):
            msg = "Password must contain at least one special character (!@#$%^&*)"
            raise ValueError(msg)
        return password


class UserRegisterResponse(BaseModel):
    """Схема данных ответа для регистрации."""

    access_token: str
