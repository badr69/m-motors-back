import pytest
from app.modules.roles.model import Role


# ======================
# FIXTURE ROLE
# ======================
@pytest.fixture()
def test_role(db_session):
    role = db_session.query(Role).filter_by(name="TEST_ROLE").first()

    if not role:
        role = Role(name="TEST_ROLE")
        db_session.add(role)
        db_session.commit()

    return role


# ======================
# CREATE ROLE
# ======================
def test_create_role(db_session):
    role = Role(name="MANAGER")
    db_session.add(role)
    db_session.commit()

    saved_role = db_session.query(Role).filter_by(name="MANAGER").first()

    assert saved_role is not None
    assert saved_role.name == "MANAGER"


# ======================
# GET ALL ROLES
# ======================
def test_get_all_roles(db_session, test_role):
    roles = db_session.query(Role).all()

    assert roles is not None
    assert len(roles) > 0


# ======================
# GET ROLE BY ID
# ======================
def test_get_role_by_id(db_session, test_role):
    role = db_session.query(Role).filter_by(id=test_role.id).first()

    assert role is not None
    assert role.id == test_role.id
    assert role.name == "TEST_ROLE"


# ======================
# UPDATE ROLE
# ======================
def test_update_role(db_session, test_role):
    test_role.name = "UPDATED_ROLE"
    db_session.commit()

    updated_role = db_session.query(Role).filter_by(id=test_role.id).first()

    assert updated_role.name == "UPDATED_ROLE"


# ======================
# DELETE ROLE
# ======================
def test_delete_role(db_session):
    role = Role(name="DELETE_ROLE")
    db_session.add(role)
    db_session.commit()

    db_session.delete(role)
    db_session.commit()

    deleted_role = db_session.query(Role).filter_by(name="DELETE_ROLE").first()

    assert deleted_role is None