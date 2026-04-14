from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import Config

# =====================
# ENGINE
# =====================
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True
)

# =====================
# SESSION
# =====================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =====================
# BASE (for models)
# =====================
Base = declarative_base()


# =====================
# DB SESSION HANDLER
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()