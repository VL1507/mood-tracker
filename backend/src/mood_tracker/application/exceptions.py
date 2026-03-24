class ApplicationError(Exception):
    """Базовая ошибка для слоя Application"""


class EmailAlreadyExistsError(ApplicationError):
    """Пользователь с таким email уже существует"""  # noqa: RUF002


class InvalidCredentialsError(ApplicationError):
    """Неверная почта или пароль"""


class InvalidRefreshTokenError(ApplicationError):
    """Неверный refresh token"""
