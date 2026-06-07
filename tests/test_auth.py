import time
import pytest

from app.modules.auth.service import AuthService
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import hash_password
from app.core.security.jwt import generate_refresh_token, decode_token


# =========================
# FIXTURE USER UNIQUE
# =========================
def create_test_user(db_session):
    unique_id = str(int(time.time() * 1000000))

    role = db_session.query(Role).filter(Role.name == "CLIENT").first()

    if not role:
        role = Role(name="CLIENT")
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)

    user = User(
        username=f"user_{unique_id}",
        email=f"user_{unique_id}@test.com",
        password_hash=hash_password("123456"),
        is_active=True,
        role_id=role.id
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


# =========================
# LOGIN SUCCESS
# =========================
def test_login_success(db_session):
    user = create_test_user(db_session)

    result = AuthService.login(db_session, user.email, "123456")

    assert result["error"] is None
    assert "access_token" in result["data"]


# =========================
# LOGIN INVALID PASSWORD
# =========================
def test_login_invalid_password(db_session):
    user = create_test_user(db_session)

    result = AuthService.login(db_session, user.email, "wrong")

    assert result["error"] == "Invalid password"


# =========================
# LOGIN USER NOT FOUND
# =========================
def test_login_user_not_found(db_session):
    result = AuthService.login(db_session, "fake@test.com", "123")

    assert result["error"] == "User not found"


# =========================
# REGISTER SUCCESS
# =========================
def test_register_success(db_session):
    result = AuthService.register(db_session, {
        "email": f"reg_{time.time()}@test.com",
        "username": f"reg_{time.time()}",
        "password": "123456"
    })

    assert result["error"] is None
    assert "access_token" in result["data"]


# =========================
# REGISTER MISSING FIELDS
# =========================
def test_register_missing_fields(db_session):
    result = AuthService.register(db_session, {})

    assert result["error"] == "Missing required fields"


# =========================
# REGISTER DUPLICATE EMAIL
# =========================
def test_register_duplicate_email(db_session):
    user = create_test_user(db_session)

    result = AuthService.register(db_session, {
        "email": user.email,
        "username": "another",
        "password": "123456"
    })

    assert result["error"] == "Email already exists"


# =========================
# CURRENT USER SUCCESS
# =========================
def test_current_user_success(db_session):
    user = create_test_user(db_session)

    result = AuthService.current_user(db_session, user.id)

    assert result["error"] is None
    assert result["data"]["email"] == user.email


# =========================
# CURRENT USER NOT FOUND
# =========================
def test_current_user_not_found(db_session):
    result = AuthService.current_user(db_session, 999999)

    assert result["error"] == "User not found"


# =========================
# REFRESH TOKEN SUCCESS
# =========================
def test_refresh_token_success(db_session):
    user = create_test_user(db_session)

    token = generate_refresh_token(user)

    result = AuthService.refresh_token(db_session, token)

    assert result["error"] is None
    assert "access_token" in result["data"]


# =========================
# REFRESH TOKEN INVALID
# =========================
def test_refresh_token_invalid():
    result = AuthService.refresh_token(None, "bad.token")

    assert result["error"] == "Invalid refresh token"


# =========================
# LOGOUT
# =========================
def test_logout():
    result = AuthService.logout()

    assert result["error"] is None
    assert result["data"]["message"] == "Logged out successfully"