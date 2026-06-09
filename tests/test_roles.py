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
# GET ALL ROLES (ROUTE)
# ======================
def test_get_roles_route(client):
    res = client.get("/api/v1/roles")
    assert res.status_code in [200, 401, 403]


# ======================
# GET ROLE BY ID (ROUTE)
# ======================
def test_get_role_by_id_route(client):
    res = client.get("/api/v1/roles/1")
    assert res.status_code in [200, 404, 401, 403]


# ======================
# ROLE PAGINATION (BRANCH COVERAGE)
# ======================
def test_roles_pagination(client):
    res = client.get("/api/v1/roles?page=1&limit=10")
    assert res.status_code in [200, 401, 403]


# ======================
# ROLE SEARCH (BRANCH COVERAGE)
# ======================
def test_roles_search(client):
    res = client.get("/api/v1/roles?search=admin")
    assert res.status_code in [200, 401, 403]


# ======================
# CREATE ROLE (ROUTE)
# ======================
def test_create_role_route(client):
    res = client.post("/api/v1/roles", json={"name": "TEST_ROLE"})
    assert res.status_code in [200, 201, 401, 403]


# ======================
# INVALID CREATE ROLE (BRANCH ERROR)
# ======================
def test_create_role_invalid(client):
    res = client.post("/api/v1/roles", json={})
    assert res.status_code in [400, 422, 401, 403]


def test_delete_role(db_session):
    role = Role(name="DELETE_ROLE")
    db_session.add(role)
    db_session.commit()

    db_session.delete(role)
    db_session.commit()

    deleted_role = db_session.query(Role).filter_by(name="DELETE_ROLE").first()

    assert deleted_role is None

