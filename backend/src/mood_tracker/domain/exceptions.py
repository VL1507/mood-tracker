class DomainError(BaseException):
    """Base domain error"""


class InvalidEmailError(DomainError):
    """Invalid email format"""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"Invalid email format: {value!r}")
