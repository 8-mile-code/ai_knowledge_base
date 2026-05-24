from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_hash() -> None:
    password = "123456"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password.startswith("$argon2")


def test_verify_password_returns_true_for_valid_password() -> None:
    password = "123456"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_returns_false_for_invalid_password() -> None:
    hashed_password = hash_password("123456")

    assert verify_password("wrong-password", hashed_password) is False


def test_create_and_decode_access_token() -> None:
    token = create_access_token(subject=1)

    payload = decode_access_token(token)

    assert payload["sub"] == "1"
