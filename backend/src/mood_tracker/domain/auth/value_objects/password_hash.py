from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PasswordHash:
    """Value object хэша пароля."""

    value: str
