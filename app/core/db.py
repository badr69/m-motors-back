from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import Config


# =====================
# DATABASE ENGINE
# =====================
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=300,
)

# =====================
# SESSION FACTORY
# =====================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# =====================
# BASE MODEL
# =====================
Base = declarative_base()

# =====================
# DATABASE SESSION
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()