from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(120), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    phone = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
    )

    role = relationship(
        "Role",
        back_populates="users",
        passive_deletes=True
    )

    rental_dossiers = relationship(
        "RentalDossier",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )