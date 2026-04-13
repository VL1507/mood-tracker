from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LoginUserInputDTO:
    """InputDTO входа в аккаунт пользователя."""

    email: str
    password: str


@dataclass(slots=True, frozen=True)
class LoginUserOutputDTO:
    """OutputDTO входа в аккаунт пользователя."""

    access_token: str
    refresh_token: str
