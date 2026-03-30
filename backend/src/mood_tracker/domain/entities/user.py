from dataclasses import dataclass

from mood_tracker.domain.value_objects import (
    PasswordHash,
    UserEmail,
    UserID,
)


@dataclass(slots=True)
class User:
    id: UserID
    email: UserEmail
    password_hash: PasswordHash

    def __eq__(self, value: object) -> bool:
        """Сущности сравниваются по идентичности (DDD)"""
        if not isinstance(value, User):
            return NotImplemented
        return self.id == value.id

    def __hash__(self) -> int:
        """Сущности хэшируются по идентичности (DDD)"""
        return hash(self.id)
