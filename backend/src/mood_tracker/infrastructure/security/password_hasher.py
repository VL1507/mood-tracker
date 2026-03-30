from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import VerifyMismatchError

from mood_tracker.domain.auth.security import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    def __init__(self) -> None:
        self._ph = Argon2PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self._ph.hash(password=password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            self._ph.verify(hash=password_hash, password=password)
        except VerifyMismatchError:
            return False
        return True
