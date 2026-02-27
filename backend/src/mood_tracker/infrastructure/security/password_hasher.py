from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from mood_tracker.domain.security import IPasswordHasher


class Argon2PasswordHasher(IPasswordHasher):
    def __init__(self) -> None:
        self._ph = PasswordHasher()

    def hash_password(self, plain_password: str) -> str:
        return self._ph.hash(password=plain_password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        try:
            self._ph.verify(hash=hashed_password, password=plain_password)
        except VerifyMismatchError:
            return False
        return True
