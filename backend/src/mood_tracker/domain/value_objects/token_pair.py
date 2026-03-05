from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenPair:
    access: str
    refresh: str
