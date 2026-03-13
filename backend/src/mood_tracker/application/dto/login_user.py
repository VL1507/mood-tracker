from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LoginUserInputDTO:
    email: str
    password: str


@dataclass(slots=True, frozen=True)
class LoginUserOutputDTO:
    access_token: str
    refresh_token: str
