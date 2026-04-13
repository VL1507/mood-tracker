from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import VerifyMismatchError

from mood_tracker.domain.auth.security import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    """Реализация IPasswordHasher на Argon2."""

    def __init__(self) -> None:
        """Инициализация PasswordHasher."""
        self._ph = Argon2PasswordHasher()

    def hash_password(self, password: str) -> str:
        """
        Хэширование пароля.

        Returns:
            str

        """
        return self._ph.hash(password=password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Верификация пароля.

        Returns:
            bool: True если прошел верификацию, False иначе

        """
        try:
            self._ph.verify(hash=password_hash, password=password)
        except VerifyMismatchError:
            return False
        return True
