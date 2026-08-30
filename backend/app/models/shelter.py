from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class ShelterStatus(str, Enum):
    OPEN = "OPEN"
    FULL = "FULL"
    CLOSED = "CLOSED"
    EMERGENCY_ONLY = "EMERGENCY_ONLY"


class Shelter(Base):
    __tablename__ = "shelters"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    current_occupancy: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    contact_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    status: Mapped[ShelterStatus] = mapped_column(
        SQLEnum(ShelterStatus),
        nullable=False,
        default=ShelterStatus.OPEN
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )