from abc import abstractmethod
from typing import Protocol


class IPasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, plain_password: str) -> str:
        pass

    @abstractmethod
    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        pass
