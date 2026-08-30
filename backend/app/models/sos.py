from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class SOSStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PRIORITIZED = "PRIORITIZED"
    ASSIGNED = "ASSIGNED"
    RESCUE_IN_PROGRESS = "RESCUE_IN_PROGRESS"
    RESCUED = "RESCUED"
    CANCELLED = "CANCELLED"


class SOSRequest(Base):
    __tablename__ = "sos_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    incident_id: Mapped[int | None] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=True
    )

    emergency_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    people_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    priority_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    status: Mapped[SOSStatus] = mapped_column(
        SQLEnum(SOSStatus),
        nullable=False,
        default=SOSStatus.RECEIVED
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )