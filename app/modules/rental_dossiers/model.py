from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class RentalDossier(Base):
    __tablename__ = "rental_dossiers"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)

    status = Column(String(20), default="pending")
    message = Column(Text, nullable=True)

    user = relationship(
        "User",
        back_populates="rental_dossiers"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="rental_dossiers"
    )

    documents = relationship(
        "Document",
        back_populates="dossier",
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