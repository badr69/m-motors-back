from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)

    # Identité véhicule
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

    # Caractéristiques
    year = Column(Integer, nullable=True)
    mileage = Column(Integer, nullable=True)

    fuel_type = Column(String(50), nullable=True)
    transmission = Column(String(50), nullable=True)

    # Prix
    price = Column(Numeric(10, 2), nullable=True)

    # Infos complémentaires
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)

    # Métier EPIC 2
    vehicle_type = Column(String(20), nullable=False)
    # "location" | "sale"

    category = Column(String(50), nullable=False)
    # citadine, suv, berline, utilitaire, sportive

    status = Column(String(20), default="available")
    # available | rented

    is_deleted = Column(Boolean, default=False)

    # Relations
    rental_dossiers = relationship(
        "RentalDossier",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    def __repr__(self):
        return f"<Vehicle {self.brand} {self.model} ({self.id})>"