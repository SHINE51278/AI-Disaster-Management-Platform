from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base
from backend.app.models.incident import IncidentSeverity


class AlertType(str, Enum):
    EARLY_WARNING = "EARLY_WARNING"
    EVACUATION = "EVACUATION"
    WEATHER_WARNING = "WEATHER_WARNING"
    EMERGENCY = "EMERGENCY"
    RECOVERY = "RECOVERY"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    alert_type: Mapped[AlertType] = mapped_column(
        SQLEnum(AlertType),
        nullable=False
    )

    severity: Mapped[IncidentSeverity] = mapped_column(
        SQLEnum(IncidentSeverity),
        nullable=False
    )

    target_area: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )