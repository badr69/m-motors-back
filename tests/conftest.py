import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.db import Base

# ======================
# TEST DATABASE (SQLite in-memory)
# ======================
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite
)

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
# FIX: OVERRIDE SESSIONLOCAL IN SERVICES
# ======================
@pytest.fixture(autouse=True)
def override_session(monkeypatch, db_session):

    # IMPORTANT: patch SessionLocal used in services
    import app.core.db as db_module

    def fake_session():
        return db_session

    monkeypatch.setattr(db_module, "SessionLocal", fake_session)