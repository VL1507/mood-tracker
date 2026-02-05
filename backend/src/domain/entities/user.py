from dataclasses import dataclass

from src.domain.value_objects.user import HashPassword, UserID, UserLogin, UserName


@dataclass(slots=True)
class User:
    id: UserID
    name: UserName
    login: UserLogin
    hash_password: HashPassword

    def __eq__(self, value) -> bool:
        if not isinstance(value, User):
            raise NotImplementedError
        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)
