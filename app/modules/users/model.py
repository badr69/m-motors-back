from datetime import datetime, UTC
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(120), unique=True, nullable=False)

    email = Column(String(120), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    phone = Column(String(30), nullable=True)

    address = Column(String(255), nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # =====================
    # RELATION ROLE
    # =====================
    role = relationship("Role", back_populates="users")

    # =====================
    # RELATION DOCUMENTS
    # =====================
    documents = relationship("Document", back_populates="user",
                             cascade="all, delete-orphan")

    # =====================
    # RELATION RENTAL DOSSIERS
    # =====================
    rental_dossiers = relationship( "RentalDossier", back_populates="user",
                                    cascade="all, delete-orphan")

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC),
                        onupdate=lambda: datetime.now(UTC))