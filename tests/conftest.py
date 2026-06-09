import os
import pytest

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.core.db import Base

from app.modules.roles.model import Role
from app.modules.users.model import User

from app.core.security.password import hash_password

# ======================
# LOAD ENV
# ======================
load_dotenv()

# ======================
# TEST DATABASE URL
# ======================
TEST_DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('TEST_DB_USER')}:"
    f"{os.getenv('TEST_DB_PASSWORD')}@"
    f"{os.getenv('TEST_DB_HOST')}:"
    f"{os.getenv('TEST_DB_PORT')}/"
    f"{os.getenv('TEST_DB_NAME')}"
)

# ======================
# ENGINE
# ======================
engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ======================
# CREATE / DROP TABLES
# ======================
@pytest.fixture(scope="session", autouse=True)
def setup_database():

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


# ======================
# FLASK APP FIXTURE
# ======================
@pytest.fixture
def app():

    app = create_app()

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URL
    app.config["JWT_SECRET_KEY"] = "test-secret"

    return app


# ======================
# FLASK CLIENT FIXTURE
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
# DB SESSION FIXTURE
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
# ADMIN USER FIXTURE
# ======================
@pytest.fixture
def admin_user(db_session):

    role = db_session.query(Role).filter_by(name="ADMIN").first()

    if not role:
        role = Role(name="ADMIN")
        db_session.add(role)
        db_session.commit()

    user = db_session.query(User).filter_by(
        email="admin@test.com"
    ).first()

    if not user:

        user = User(
            email="admin@test.com",
            password=hash_password("admin"),
            role_id=role.id
        )

        db_session.add(user)
        db_session.commit()

    return user


# ======================
# ADMIN TOKEN FIXTURE
# ======================
@pytest.fixture
def token_admin(client, admin_user):

    res = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "admin"
        }
    )

    data = res.get_json()

    assert res.status_code == 200, f"Login failed: {data}"

    assert data is not None
    assert "access_token" in data

    return data["access_token"]










#
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from app.core.db import Base
# from app import create_app
#
# # ======================
# # TEST DATABASE (SQLite in-memory)
# # ======================
# TEST_DATABASE_URL = "sqlite:///:memory:"
#
# engine = create_engine(
#     TEST_DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )
#
# TestingSessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )
#
# # ======================
# # CREATE / DROP TABLES
# # ======================
# @pytest.fixture(scope="session", autouse=True)
# def setup_database():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)
#
#
# # ======================
# # FLASK APP FIXTURE
# # ======================
# @pytest.fixture
# def app():
#     app = create_app()
#
#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URL
#     app.config["JWT_SECRET_KEY"] = "test-secret"
#
#     return app
#
#
# # ======================
# # FLASK CLIENT FIXTURE
# # ======================
# @pytest.fixture
# def client(app):
#     return app.test_client()
#
#
# # ======================
# # APP CONTEXT
# # ======================
# @pytest.fixture(autouse=True)
# def app_context(app):
#     with app.app_context():
#         yield
#
#
# # ======================
# # DB SESSION FIXTURE
# # ======================
# @pytest.fixture()
# def db_session():
#
#     session = TestingSessionLocal()
#
#     try:
#         yield session
#     finally:
#         session.rollback()
#         session.close()
#
#
# # ======================
# # OVERRIDE SESSION (IMPORTANT)
# # ======================
# @pytest.fixture(autouse=True)
# def override_session(monkeypatch, db_session):
#
#     import app.core.db as db_module
#
#     def fake_session():
#         return db_session
#
#     monkeypatch.setattr(db_module, "SessionLocal", fake_session)
#
#
# # ======================
# # ADMIN TOKEN FIXTURE
# # ======================
# import pytest
#
# @pytest.fixture
# def token_admin(client):
#
#     res = client.post("/api/v1/auth/login", json={
#         "email": "admin@test.com",
#         "password": "admin"
#     })
#
#     data = res.get_json()
#
#     # 🔥 FAIL FAST (IMPORTANT)
#     assert res.status_code == 200, f"Login failed: {data}"
#
#     assert data is not None, "No response body from login"
#     assert "access_token" in data, f"No token in response: {data}"
#
#     return data["access_token"]
#
#
