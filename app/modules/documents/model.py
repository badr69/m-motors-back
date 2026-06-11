from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from sqlalchemy.orm import relationship

from app.core.db import Base


class Document(Base):

    __tablename__ = "documents"

    # =====================
    # PRIMARY KEY
    # =====================
    id = Column(Integer, primary_key=True)

    # =====================
    # RELATIONS
    # =====================
    dossier_id = Column(
        Integer,
        ForeignKey("rental_dossiers.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # =====================
    # DOCUMENT INFO
    # =====================
    type_document = Column(
        String(50),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    filepath = Column(
        Text,
        nullable=False
    )

    mime_type = Column(
        String(100),
        nullable=False
    )

    # =====================
    # RELATIONS
    # =====================
    dossier = relationship(
        "RentalDossier",
        back_populates="documents"
    )

    user = relationship(
        "User",
        back_populates="documents"
    )

    # =====================
    # TIMESTAMPS
    # =====================
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )