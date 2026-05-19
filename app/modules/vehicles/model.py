from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)

    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

    year = Column(Integer, nullable=True)
    mileage = Column(Integer, nullable=True)

    fuel_type = Column(String(50), nullable=True)
    transmission = Column(String(50), nullable=True)

    price = Column(Numeric(10, 2), nullable=True)

    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)

    availability = Column(Boolean, default=True)

    status = Column(String(20), default="location")

    rental_dossiers = relationship(
        "RentalDossier",
        back_populates="vehicle",
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