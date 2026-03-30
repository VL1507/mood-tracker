class DomainError(Exception):
    """Базовая ошибка для доменного слоя"""


class InvalidEmailError(DomainError):
    """Невалидный формат email"""

    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid email format: {value!r}")
