from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UserEmail:
    value: str
