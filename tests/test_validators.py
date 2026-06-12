from app.core.validators import (
    validate_email,
    validate_password,
    validate_username,
    validate_login,
    validate_register,
    validate_required
)

# ======================
# EMAIL
# ======================
def test_validate_email_valid():
    assert validate_email("test@test.com") is None


def test_validate_email_invalid():
    assert validate_email("bad-email") == "Invalid email format"


def test_validate_email_required():
    assert validate_email(None) == "Email is required"


# ======================
# PASSWORD
# ======================
def test_validate_password_valid():
    assert validate_password("123456") is None


def test_validate_password_required():
    assert validate_password(None) == "Password is required"


def test_validate_password_too_short():
    assert validate_password("123") == "Password must be at least 6 characters"


def test_validate_password_too_long():
    assert validate_password("x" * 101) == "Password too long"


# ======================
# USERNAME
# ======================
def test_validate_username_valid():
    assert validate_username("badr") is None


def test_validate_username_required():
    assert validate_username(None) == "Username is required"


def test_validate_username_too_short():
    assert validate_username("ab") == "Username must be at least 3 characters"


def test_validate_username_too_long():
    assert validate_username("x" * 51) == "Username too long"


# ======================
# LOGIN
# ======================
def test_validate_login_email_error():
    assert validate_login({
        "email": "bad-email",
        "password": "123456"
    }) == "Invalid email format"


def test_validate_login_password_error():
    assert validate_login({
        "email": "test@test.com",
        "password": "123"
    }) == "Password must be at least 6 characters"


def test_validate_login_success():
    assert validate_login({
        "email": "test@test.com",
        "password": "123456"
    }) is None


# ======================
# REGISTER
# ======================
def test_validate_register_username_error():
    assert validate_register({
        "username": "ab",
        "email": "test@test.com",
        "password": "123456"
    }) == "Username must be at least 3 characters"


def test_validate_register_success():
    assert validate_register({
        "username": "badr",
        "email": "test@test.com",
        "password": "123456"
    }) is None


# ======================
# REQUIRED FIELD
# ======================
def test_validate_required():
    assert validate_required(None, "email") == "email is required"
    assert validate_required("ok", "email") is None