import pytest

from mood_tracker.domain.auth.value_objects import UserEmail
from mood_tracker.domain.exceptions import InvalidEmailError


@pytest.mark.parametrize(
    ("email_str", "expected"),
    [
        ("test@example.com", "test@example.com"),
        ("  Test@Example.COM  ", "test@example.com"),
        ("user+tag@sub.domain.io", "user+tag@sub.domain.io"),
        ("tes-t@qq-example.com", "tes-t@qq-example.com"),
    ],
)
def test_valid_email(email_str: str, expected: str) -> None:
    email = UserEmail(value=email_str)
    assert email.value == expected


@pytest.mark.parametrize(
    "email_str",
    [
        "testexample.com",
        "test@examplecom",
        "@example.com",
        "test@",
        "test@.com",
        "@.",
        "r @r . r",
        "@",
        "",
    ],
)
def test_invalid_email(email_str: str) -> None:
    with pytest.raises(InvalidEmailError):
        UserEmail(value=email_str)
