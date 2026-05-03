from datetime import datetime, UTC
from app.core.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)

    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role")

    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(UTC))

    updated_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


