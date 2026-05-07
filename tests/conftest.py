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
        yield app

# ======================
# DB SESSION (clean per test)
# ======================
@pytest.fixture()
def db_session(app):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================
# CLIENT
# ======================
@pytest.fixture()
def client(app, db_session):
    return app.test_client()









# import pytest
# from app import create_app
# from app.core.config import TestConfig
# from app.core.db import Base, engine, SessionLocal
#
#
# # ======================
# # APP TEST
# # ======================
# @pytest.fixture(scope="session")
# def app():
#     app = create_app()
#     app.config.from_object(TestConfig)
#
#     with app.app_context():
#         print("TEST DB =>", app.config["SQLALCHEMY_DATABASE_URI"])
#
#         Base.metadata.drop_all(bind=engine)
#         Base.metadata.create_all(bind=engine)
#
#         yield app
#
#         Base.metadata.drop_all(bind=engine)
#
#
# # ======================
# # DB SESSION ISOLÉE
# # ======================
# @pytest.fixture()
# def db_session():
#     connection = engine.connect()
#     transaction = connection.begin()
#
#     session = SessionLocal(bind=connection)
#
#     yield session
#
#     session.close()
#     transaction.rollback()
#     connection.close()
#
#
# # ======================
# # CLIENT
# # ======================
# @pytest.fixture(scope="session")
# def client(app):
#     return app.test_client()