from mood_tracker.shared.domain.exceptions import DomainError


class InvalidEmailError(DomainError):
    """Невалидный формат email."""

    def __init__(self, value: str) -> None:
        """Инициализация InvalidEmailError."""
        super().__init__(f"Invalid email format: {value!r}")
