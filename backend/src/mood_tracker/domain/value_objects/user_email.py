import re
from dataclasses import dataclass

from mood_tracker.domain.exceptions import InvalidEmailError


@dataclass(slots=True, frozen=True)
class UserEmail:
    value: str

    def __post_init__(self) -> None:
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, self.value):
            raise InvalidEmailError(self.value)
