# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import Config

# =====================
# DATABASE URL
# =====================
DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI

# =====================
# ENGINE
# =====================git status

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

# =====================
# SESSION
# =====================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# =====================
# BASE
# =====================
Base = declarative_base()

# =====================
# DB SESSION
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()