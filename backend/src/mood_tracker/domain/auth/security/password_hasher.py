from abc import abstractmethod
from typing import Protocol


class IPasswordHasher(Protocol):
    """Протокол для хэширования паролей."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Хэширование пароля."""

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Верификация пароля."""
