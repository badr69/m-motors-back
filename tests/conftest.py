import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.core.db import Base
import app.core.db as db_module

from app.modules.roles.model import Role
from app.modules.users.model import User
from app.core.security.password import hash_password


# ======================
# SQLITE TEST DB
# ======================
TEST_DATABASE_URL = "sqlite:///./test_db.sqlite"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# override session
db_module.SessionLocal = TestingSessionLocal


# ======================
# DB INIT
# ======================
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ======================
# APP
# ======================
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret"
    return app


# ======================
# CLIENT
# ======================
@pytest.fixture
def client(app):
    return app.test_client()


# ======================
# APP CONTEXT
# ======================
@pytest.fixture(autouse=True)
def app_context(app):
    with app.app_context():
        yield


# ======================
# DB SESSION
# ======================
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ======================
# ADMIN USER
# ======================
@pytest.fixture
def admin_user(db_session):

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
            password_hash=hash_password("admin"),
            role_id=role.id
        )
        db_session.add(user)
        db_session.commit()

    return user


# ======================
# ADMIN TOKEN
# ======================
@pytest.fixture
def token_admin(client, admin_user):

    res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "admin"
    })

    data = res.get_json()
    assert res.status_code == 200

    return data["access_token"]


# ======================
# CLIENT USER
# ======================
@pytest.fixture
def normal_user(db_session):

    role = db_session.query(Role).filter_by(name="CLIENT").first()
    if not role:
        role = Role(name="CLIENT")
        db_session.add(role)
        db_session.commit()

    user = db_session.query(User).filter_by(email="user@test.com").first()
    if not user:
        user = User(
            username="user",
            email="user@test.com",
            password_hash=hash_password("user"),
            role_id=role.id
        )
        db_session.add(user)
        db_session.commit()

    return user


# ======================
# USER TOKEN
# ======================
@pytest.fixture
def token_user(client, normal_user):

    res = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "user"
    })

    data = res.get_json()
    assert res.status_code == 200

    return data["access_token"]


# ======================
# VEHICLE
# ======================
@pytest.fixture
def vehicle(db_session):

    from app.modules.vehicles.model import Vehicle

    v = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2022,
        mileage=10000,
        fuel_type="petrol",
        transmission="manual",
        price=15000,
        description="Test vehicle",
        image_url=None,
        category="SUV",
        vehicle_type="location",
        status="available"
    )

    db_session.add(v)
    db_session.commit()
    db_session.refresh(v)

    return v


# ======================
# DOSSIER (IMPORTANT)
# ======================
@pytest.fixture
def dossier(client, token_user, vehicle):

    res = client.post(
        "/api/v1/rental_dossiers",
        json={
            "vehicle_id": vehicle.id,
            "message": "test dossier"
        },
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    data = res.get_json()
    assert res.status_code == 201

    return data["data"]


@pytest.fixture
def document(client, token_user, dossier):

    import io

    data = {
        "dossier_id": str(dossier["id"]),
        "type_document": "identity",
        "file": (
            io.BytesIO(b"fake pdf content"),
            "test.pdf"
        )
    }

    response = client.post(
        "/api/v1/documents",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": f"Bearer {token_user}"
        }
    )

    assert response.status_code == 201

    return response.get_json()["data"]
