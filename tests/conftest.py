import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.db import Base


# ======================
# TEST DATABASE URL
# ======================
TEST_DATABASE_URL = "postgresql+psycopg2://badr:Setif_19000@postgresql-badr.alwaysdata.net:5432/badr_m_motors_test_db"

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
# SETUP / TEARDOWN DB
# ======================
@pytest.fixture(scope="session", autouse=True)
def setup_database():

    # DROP + CREATE SAFE (gère FK automatiquement)
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine)

    yield

    # Base.metadata.drop_all(bind=engine, checkfirst=True)


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







#