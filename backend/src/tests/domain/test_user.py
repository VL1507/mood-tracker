from mood_tracker.domain.entities import User
from mood_tracker.domain.value_objects import PasswordHash, UserEmail, UserID


def test_user_fields() -> None:
    uid = UserID.new()
    email = UserEmail("user@example.com")
    password_hash = PasswordHash("ph")

    user = User(id=uid, email=email, password_hash=password_hash)

    assert user.id == uid
    assert user.email == email
    assert user.password_hash == password_hash


def test_eq_same_id() -> None:
    uid = UserID.new()
    u1 = User(
        id=uid,
        email=UserEmail("u1@example.com"),
        password_hash=PasswordHash("u1"),
    )
    u2 = User(
        id=uid,
        email=UserEmail("u2@example.com"),
        password_hash=PasswordHash("u2"),
    )
    assert u1 == u2


def test_eq_different_id() -> None:
    u1 = User(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
    )
    u2 = User(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
    )
    assert u1 != u2


def test_eq_not_implemented_for_other_types() -> None:
    u = User(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
    )
    result = u.__eq__("not a user")  # noqa: PLC2801
    assert result is NotImplemented


def test_hash_same_id() -> None:
    uid = UserID.new()
    u1 = User(
        id=uid,
        email=UserEmail("u1@example.com"),
        password_hash=PasswordHash("ph1"),
    )
    u2 = User(
        id=uid,
        email=UserEmail("u2@example.com"),
        password_hash=PasswordHash("ph1"),
    )
    assert hash(u1) == hash(u2)


def test_hash_different_id() -> None:
    u1 = User(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
    )
    u2 = User(
        id=UserID.new(),
        email=UserEmail("user@example.com"),
        password_hash=PasswordHash("ph"),
    )
    assert hash(u1) != hash(u2)
