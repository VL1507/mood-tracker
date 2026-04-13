from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RefreshUserInputDTO:
    """InputDTO обновления токенов пользователя."""

    refresh_token: str


@dataclass(slots=True, frozen=True)
class RefreshUserOutputDTO:
    """OutputDTO обновления токенов пользователя."""

    access_token: str
    refresh_token: str
