from abc import abstractmethod
from typing import Protocol


class IPasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...
    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool: ...
