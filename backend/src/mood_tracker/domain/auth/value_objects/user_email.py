import re
from dataclasses import dataclass

from mood_tracker.domain.exceptions import InvalidEmailError

_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


@dataclass(slots=True, frozen=True)
class UserEmail:
    """Raises:
    InvalidEmailError: невалидный формат email

    """

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not _EMAIL_PATTERN.fullmatch(normalized):
            raise InvalidEmailError(self.value)
        object.__setattr__(self, "value", normalized)
