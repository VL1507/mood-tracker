from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HashPassword:
    value: str
