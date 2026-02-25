from dataclasses import dataclass

from mood_tracker.domain.value_objects import (
    HashPassword,
    UserEmail,
    UserID,
)


@dataclass(slots=True)
class User:
    id: UserID
    email: UserEmail
    hash_password: HashPassword

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, User):
            raise NotImplementedError
        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)
