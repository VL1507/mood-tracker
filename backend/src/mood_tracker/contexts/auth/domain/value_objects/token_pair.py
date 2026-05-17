from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenPair:
    """Value object пары токенов access и refresh."""

    access_token: str
    refresh_token: str
