from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegisterUserInputDTO:
    """InputDTO регистрации пользователя."""

    email: str
    password: str


@dataclass(slots=True, frozen=True)
class RegisterUserOutputDTO:
    """OutputDTO регистрации пользователя."""

    access_token: str
    refresh_token: str
