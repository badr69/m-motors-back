from app.core.security.password import hash_password, verify_password
from app.core.security.jwt import generate_access_token, decode_token


class DummyRole:
    name = "ADMIN"


class DummyUser:
    id = 1
    email = "admin@test.com"
    role = DummyRole()


def test_hash_password():
    password = "Admin123!"
    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password():
    password = "Admin123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_generate_access_token():
    user = DummyUser()
    token = generate_access_token(user)

    assert token is not None
    assert isinstance(token, str)


def test_decode_access_token():
    user = DummyUser()
    token = generate_access_token(user)

    payload = decode_token(token)

    assert payload["user_id"] == 1
    assert payload["email"] == "admin@test.com"
    assert payload["role"] == "ADMIN"
    assert payload["type"] == "access"