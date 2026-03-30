from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
