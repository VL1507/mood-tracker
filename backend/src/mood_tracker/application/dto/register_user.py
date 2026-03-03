from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegisterUserInputDTO:
    email: str
    password: str
