from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4


@dataclass(slots=True, frozen=True)
class UserID:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(uuid4())

    @classmethod
    def from_str(cls, uuid_str: str) -> Self:
        return cls(UUID(uuid_str))
