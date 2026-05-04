import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # =====================
    # FLASK
    # =====================
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("FLASK_ENV") == "development"

    # =====================
    # JWT
    # =====================
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 2))

    # =====================
    # DATABASE
    # =====================
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TEST_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_TEST_DATABASE_URI
    TESTING = True






# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
#
# class Config:
#     # =====================
#     # FLASK
#     # =====================
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     DEBUG = os.getenv("FLASK_ENV") == "development"
#
#     # =====================
#     # JWT
#     # =====================
#     JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 2))
#
#     # =====================
#     # DATABASE (DEV)
#     # =====================
#     DB_HOST = os.getenv("DB_HOST")
#     DB_PORT = os.getenv("DB_PORT")
#     DB_NAME = os.getenv("DB_NAME")
#     DB_USER = os.getenv("DB_USER")
#     DB_PASSWORD = os.getenv("DB_PASSWORD")
#
#     SQLALCHEMY_DATABASE_URI = (
#         f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
#         f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )
#
#     # =====================
#     # DATABASE (TEST)
#     # =====================
#     TEST_DB_NAME = os.getenv("TEST_DB_NAME")
#
#     SQLALCHEMY_TEST_DATABASE_URI = (
#         f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
#         f"@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
#     )
#
#
# class TestConfig(Config):
#     SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_TEST_DATABASE_URI
#     TESTING = True