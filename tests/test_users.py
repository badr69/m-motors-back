import pytest
from werkzeug.security import generate_password_hash

from app.modules.users.model import User
from app.modules.roles.model import Role
from app.modules.users.service import UserService


# ======================
# FIXTURE ROLE
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
# FIXTURE USER
# ======================
@pytest.fixture()
def test_user(db_session, user_role):

    user = db_session.query(User).filter_by(
        email="test@test.com"
    ).first()

    if not user:
        user = User(
            username="testuser",
            email="test@test.com",
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
# CREATE USER
# ======================
def test_create_user(db_session, user_role):

    data = {
        "username": "newuser",
        "email": "new@test.com",
        "password": "123456",
        "phone": "0611111111",
        "address": "Paris",
        "role_id": user_role.id
    }

    result = UserService.create_user(db_session, data)

    assert result["error"] is None
    assert result["data"]["email"] == "new@test.com"


# ======================
# GET USER BY ID
# ======================
def test_get_user_by_id(db_session, test_user):

    result = UserService.get_user_by_id(
        db_session,
        test_user.id
    )

    assert result["error"] is None
    assert result["data"]["email"] == "test@test.com"


# ======================
# UPDATE USER
# ======================
def test_update_user(db_session, test_user):

    result = UserService.update_user(
        db_session,
        test_user.id,
        {"phone": "0699999999"}
    )

    assert result["error"] is None
    assert result["data"]["phone"] == "0699999999"


# ======================
# DELETE USER
# ======================
def test_delete_user(db_session, user_role):

    user = User(
        username="deleteuser",
        email="delete@test.com",
        password_hash=generate_password_hash("123456"),
        role_id=user_role.id,
        is_active=True
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    result = UserService.delete_user(
        db_session,
        user.id
    )

    assert result["error"] is None
    assert result["data"]["message"] == "User deleted successfully"


# ======================
# GET ME
# ======================
def test_get_me(db_session, test_user):

    current_user = {
        "user_id": test_user.id,
        "email": test_user.email,
        "role": "USER"
    }

    result = UserService.get_me(
        db_session,
        current_user
    )

    assert result["error"] is None
    assert result["data"]["email"] == test_user.email


# ======================
# UPDATE ME
# ======================
def test_update_me(db_session, test_user):

    current_user = {
        "user_id": test_user.id,
        "email": test_user.email,
        "role": "USER"
    }

    result = UserService.update_me(
        db_session,
        current_user,
        {"phone": "0700000000"}
    )

    assert result["error"] is None
    assert result["data"]["phone"] == "0700000000"


# ======================
# DELETE ME
# ======================
def test_delete_me(db_session, user_role):

    user = User(
        username="meuser",
        email="me@test.com",
        password_hash=generate_password_hash("123456"),
        role_id=user_role.id,
        is_active=True
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    current_user = {
        "user_id": user.id,
        "email": user.email,
        "role": "USER"
    }

    result = UserService.delete_me(
        db_session,
        current_user
    )

    assert result["error"] is None
    assert result["data"]["message"] == "User deleted successfully"