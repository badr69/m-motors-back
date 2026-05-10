from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

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

    filename = Column(String(255), nullable=False)
    filepath = Column(Text, nullable=False)
    mime_type = Column(String(100), nullable=True)

    dossier = relationship(
        "RentalDossier",
        back_populates="documents"
    )

    user = relationship(
        "User",
        back_populates="documents"
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )