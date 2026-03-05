from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegisterUserInputDTO:
    email: str
    password: str


@dataclass(slots=True, frozen=True)
class RegisterUserOutputDTO:
    access_token: str
    refresh_token: str
