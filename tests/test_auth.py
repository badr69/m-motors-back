import pytest
from app.modules.auth.service import AuthService
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.core.security.password import hash_password


# ======================
# FIXTURE USER
# ======================
@pytest.fixture()
def test_user(db_session):
    role = db_session.query(Role).filter_by(name="ADMIN").first()

    if not role:
        role = Role(name="ADMIN")
        db_session.add(role)
        db_session.commit()

    user = db_session.query(User).filter_by(email="admin@test.com").first()

    if not user:
        user = User(
            username="admin",
            email="admin@test.com",
            password=hash_password("Admin123!"),
            role_id=role.id
        )
        db_session.add(user)
        db_session.commit()

    return user


# ======================
# LOGIN SUCCESS
# ======================
def test_login_success(db_session, test_user):
    result, error = AuthService.login(
        db_session,
        "admin@test.com",
        "Admin123!"
    )

    assert error is None
    assert result is not None
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["user"]["email"] == "admin@test.com"


# ======================
# LOGIN USER NOT FOUND
# ======================
def test_login_user_not_found(db_session):
    result, error = AuthService.login(
        db_session,
        "ghost@test.com",
        "Admin123!"
    )

    assert result is None
    assert error == "User not found"


# ======================
# LOGIN WRONG PASSWORD
# ======================
def test_login_wrong_password(db_session, test_user):
    result, error = AuthService.login(
        db_session,
        "admin@test.com",
        "WrongPassword"
    )

    assert result is None
    assert error == "Invalid password"