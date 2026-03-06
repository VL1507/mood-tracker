class DomainError(Exception): ...


class InvalidEmailError(DomainError):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid email format: {value!r}")
