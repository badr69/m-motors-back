import pytest
import time
from werkzeug.security import generate_password_hash

from app.modules.users.model import User
from app.modules.roles.model import Role
from app.modules.users.service import UserService


# ======================
# FIXTURE ROLE SAFE
# ======================
@pytest.fixture()
def user_role(db_session):
    role = db_session.query(Role).filter_by(name="USER").first()
    if not role:
        role = Role(name="USER")
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)
    return role


# ======================
# FIXTURE USER SAFE
# ======================
@pytest.fixture()
def test_user(db_session, user_role):
    unique = str(int(time.time() * 1000000))
    user = User(
        username=f"test_{unique}",
        email=f"test_{unique}@test.com",
        password_hash=generate_password_hash("123456"),
        phone="0600000000",
        address="Lyon",
        role_id=user_role.id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ======================
# SERVICE TESTS
# ======================
def test_create_user(db_session, user_role):
    unique = str(int(time.time() * 1000000))
    data = {
        "username": f"new_{unique}",
        "email": f"new_{unique}@test.com",
        "password": "123456",
        "phone": "0611111111",
        "address": "Paris",
        "role_id": user_role.id
    }
    result = UserService.create_user(db_session, data)
    assert result["error"] is None
    assert result["data"]["email"].startswith("new_")


def test_get_user_by_id(db_session, test_user):
    current_user = {"user_id": test_user.id, "role": "ADMIN"}
    result = UserService.get_user_by_id(db_session, current_user, test_user.id)
    assert result["error"] is None
    assert result["data"]["email"] == test_user.email


def test_update_user(db_session, test_user):
    result = UserService.update_user(db_session, test_user.id, {"phone": "0699999999"})
    assert result["error"] is None
    assert result["data"]["phone"] == "0699999999"


def test_delete_user(db_session, user_role):
    user = User(
        username=f"delete_{time.time()}",
        email=f"delete_{time.time()}@test.com",
        password_hash=generate_password_hash("123456"),
        role_id=user_role.id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    result = UserService.delete_user(db_session, user.id)
    assert result["error"] is None
    assert result["data"]["message"] == "User deleted successfully"


def test_get_me(db_session, test_user):
    current_user = {"user_id": test_user.id, "role": "USER"}
    result = UserService.get_me(db_session, current_user)
    assert result["error"] is None
    assert result["data"]["email"] == test_user.email


def test_update_me(db_session, test_user):
    current_user = {"user_id": test_user.id, "role": "USER"}
    result = UserService.update_me(db_session, current_user, {"phone": "0700000000"})
    assert result["error"] is None
    assert result["data"]["phone"] == "0700000000"


def test_delete_me(db_session, test_user):
    result = UserService.delete_me(db_session, test_user.id)
    assert result["error"] is None
    assert result["data"]["message"] == "User deleted successfully"