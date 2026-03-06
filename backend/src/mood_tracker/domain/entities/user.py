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
        if not isinstance(value, User):
            return NotImplemented
        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)
