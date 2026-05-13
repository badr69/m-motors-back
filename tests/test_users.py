import pytest
from werkzeug.security import generate_password_hash

from app.modules.users.model import User
from app.modules.roles.model import Role


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

    return user


# ======================
# CREATE USER
# ======================
def test_create_user(db_session, user_role):

    user = User(
        username="newuser",
        email="new@test.com",
        password_hash=generate_password_hash("123456"),
        phone="0611111111",
        address="Paris",
        role_id=user_role.id,
        is_active=True
    )

    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(
        email="new@test.com"
    ).first()

    assert saved_user is not None
    assert saved_user.username == "newuser"


# ======================
# GET USER BY ID
# ======================
def test_get_user_by_id(db_session, test_user):

    user = db_session.query(User).filter_by(
        id=test_user.id
    ).first()

    assert user is not None
    assert user.email == "test@test.com"


# ======================
# UPDATE USER
# ======================
def test_update_user(db_session, test_user):

    test_user.phone = "0699999999"

    db_session.commit()

    updated_user = db_session.query(User).filter_by(
        id=test_user.id
    ).first()

    assert updated_user.phone == "0699999999"


# ======================
# DELETE USER
# ======================
def test_delete_user(db_session, user_role):

    user = User(
        username="deleteuser",
        email="delete@test.com",
        password_hash=generate_password_hash("123456"),
        role_id=user_role.id
    )

    db_session.add(user)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    deleted_user = db_session.query(User).filter_by(
        email="delete@test.com"
    ).first()

    assert deleted_user is None