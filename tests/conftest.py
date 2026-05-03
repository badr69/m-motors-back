import pytest
from app import create_app
from app.core.db import Base, engine, SessionLocal


# ======================
# APP TEST
# ======================
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        from app.core.config import Config
        print("TEST DB =>", Config.SQLALCHEMY_DATABASE_URI)
        Base.metadata.create_all(bind=engine)
        yield app
        # Base.metadata.drop_all(bind=engine)
        print(Base.metadata.tables.keys())

# ======================
# DB SESSION
# ======================
@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# CLIENT
# ======================
@pytest.fixture(scope="session")
def client(app):
    return app.test_client()