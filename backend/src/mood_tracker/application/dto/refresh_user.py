from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RefreshUserInputDTO:
    refresh_token: str


@dataclass(slots=True, frozen=True)
class RefreshUserOutputDTO:
    access_token: str
    refresh_token: str
