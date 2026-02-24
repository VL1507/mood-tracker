import re
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UserEmail:
    value: str

    def __post_init__(self) -> None:
        # TODO: найти хороший паттерн
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, self.value):
            # TODO: заменить ошибку
            raise ValueError
