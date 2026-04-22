from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4


@dataclass(slots=True, frozen=True)
class UserID:
    """Value object ID пользователя."""

    value: UUID

    @classmethod
    def new(cls) -> Self:
        """
        Генерация нового UserID.

        Returns:
            UserID

        """
        return cls(uuid4())

    @classmethod
    def from_str(cls, uuid_str: str) -> Self:
        """
        Получение UserID из строки str.

        Returns:
            UserID

        """
        return cls(UUID(uuid_str))
