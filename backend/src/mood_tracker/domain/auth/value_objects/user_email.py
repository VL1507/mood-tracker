import re
from dataclasses import dataclass

from mood_tracker.domain.exceptions import InvalidEmailError

_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._+-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")


@dataclass(slots=True, frozen=True)
class UserEmail:
    """Value object почты пользователя."""

    value: str

    def __post_init__(self) -> None:
        """
        Нормалиция и проверка формата.

        Raises:
            InvalidEmailError: строка не проходит проверку на формат почты

        """
        normalized = self.value.strip().lower()
        if not _EMAIL_PATTERN.fullmatch(normalized):
            raise InvalidEmailError(self.value)
        object.__setattr__(self, "value", normalized)
