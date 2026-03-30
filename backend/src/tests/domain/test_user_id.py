import uuid

import pytest

from mood_tracker.domain.value_objects import UserID


def test_user_id_fields() -> None:
    uuid_4 = uuid.uuid4()
    uid = UserID(value=uuid_4)

    assert uid.value == uuid_4


def test_generate_different_ids() -> None:
    assert UserID.new() != UserID.new()


def test_from_str_valid() -> None:
    uuid_4 = uuid.uuid4()
    uid = UserID.from_str(uuid_str=str(uuid_4))

    assert uid.value == uuid_4


def test_from_str_invalid() -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        UserID.from_str("not-a-uuid")


def test_eq_same_value() -> None:
    uuid_4 = uuid.uuid4()
    assert UserID(value=uuid_4) == UserID(value=uuid_4)


def test_immutable() -> None:
    uid = UserID.new()
    with pytest.raises(AttributeError):
        uid.value = uuid.uuid4()  # type: ignore  # noqa: PGH003


def test_from_str_roundtrip() -> None:
    uid = UserID.new()
    assert UserID.from_str(str(uid.value)) == uid


def test_hashable() -> None:
    uid = UserID.new()
    assert {uid: "ok"}[uid] == "ok"
