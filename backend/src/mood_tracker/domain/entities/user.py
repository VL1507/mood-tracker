from dataclasses import dataclass

from mood_tracker.domain.value_objects.hash_password import HashPassword
from mood_tracker.domain.value_objects.user_email import UserEmail
from mood_tracker.domain.value_objects.user_id import UserID
from mood_tracker.domain.value_objects.user_name import UserName


@dataclass(slots=True)
class User:
    id: UserID
    name: UserName
    email: UserEmail
    hash_password: HashPassword

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, User):
            raise NotImplementedError
        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)
