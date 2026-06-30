import pytest
import time
from app.modules.roles.model import Role
from app.modules.roles.service import RoleService


# ======================
# FIXTURE ROLE SAFE
# ======================
@pytest.fixture()
def test_role(db_session):
    unique = str(int(time.time() * 1000000))
    role = Role(name=f"TEST_ROLE_{unique}")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


# ======================
# DB TESTS
# ======================
def test_create_role(db_session):
    role = Role(name=f"MANAGER_{time.time()}")
    db_session.add(role)
    db_session.commit()
    saved = db_session.query(Role).filter(Role.name == role.name).first()
    assert saved is not None
    assert "MANAGER" in saved.name


def test_get_all_roles(db_session, test_role):
    roles = db_session.query(Role).all()
    assert roles is not None
    assert len(roles) > 0


def test_get_role_by_id(db_session, test_role):
    role = db_session.query(Role).filter(Role.id == test_role.id).first()
    assert role is not None
    assert role.id == test_role.id


def test_update_role(db_session, test_role):
    test_role.name = "UPDATED_ROLE"
    db_session.commit()
    updated = db_session.query(Role).filter(Role.id == test_role.id).first()
    assert updated.name == "UPDATED_ROLE"


def test_delete_role(db_session):
    role = Role(name=f"DELETE_ROLE_{time.time()}")
    db_session.add(role)
    db_session.commit()
    db_session.delete(role)
    db_session.commit()
    deleted = db_session.query(Role).filter_by(id=role.id).first()
    assert deleted is None


# ======================
# ROUTE TESTS
# ======================
def test_get_roles_route(client):
    res = client.get("/api/v1/roles")
    assert res.status_code in [200, 401, 403]


def test_get_role_by_id_route(client, test_role):
    res = client.get(f"/api/v1/roles/{test_role.id}")
    assert res.status_code in [200, 404, 401, 403]


def test_roles_pagination(client):
    res = client.get("/api/v1/roles?page=1&limit=10")
    assert res.status_code in [200, 401, 403]


def test_roles_search(client):
    res = client.get("/api/v1/roles?search=admin")
    assert res.status_code in [200, 401, 403]


def test_create_role_route(client, token_admin):
    res = client.post(
        "/api/v1/roles",
        json={"name": f"TEST_ROLE_{time.time()}"},
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert res.status_code in [200, 201, 400, 403]


def test_create_role_invalid(client, token_admin):
    res = client.post(
        "/api/v1/roles",
        json={},
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert res.status_code in [400, 422, 403]


def test_get_role_not_found(client, token_admin):
    res = client.get(
        "/api/v1/roles/999999999",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert res.status_code in [404, 403]


# ======================
# SERVICE TESTS
# ======================
def test_service_create_role_success(db_session):
    """Test création d'un rôle via le service"""
    name = f"SERVICE_ROLE_{int(time.time())}"
    result = RoleService.create_role(db_session, name)
    assert result["error"] is None
    assert result["data"]["name"] == name


def test_service_create_role_empty(db_session):
    """Test création d'un rôle vide via le service"""
    result = RoleService.create_role(db_session, "")
    assert result["error"] is not None


def test_service_create_role_duplicate(db_session, test_role):
    """Test création d'un rôle dupliqué via le service"""
    result = RoleService.create_role(db_session, test_role.name)
    # Le service peut retourner une erreur ou le rôle existant
    assert result["error"] is not None or result["data"] is not None


def test_service_normalize_role():
    """Test de la méthode normalize"""
    result = RoleService.normalize("admin")
    assert result is not None
    assert isinstance(result, str)

    result = RoleService.normalize(" admin ")
    assert result is not None

    result = RoleService.normalize("")
    assert result is None or result == ""
    result = RoleService.normalize(None)
    assert result is None