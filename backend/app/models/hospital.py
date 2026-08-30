from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class HospitalStatus(str, Enum):
    OPEN = "OPEN"
    FULL = "FULL"
    CLOSED = "CLOSED"


class Hospital(Base):
    __tablename__ = "hospitals"

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

    emergency_capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    available_beds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    contact_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    status: Mapped[HospitalStatus] = mapped_column(
        SQLEnum(HospitalStatus),
        nullable=False,
        default=HospitalStatus.OPEN
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