from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    String,
    Text,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class DamageLevel(str, Enum):
    NONE = "NONE"
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"
    DESTROYED = "DESTROYED"


class DamageReport(Base):
    __tablename__ = "damage_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False
    )

    image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    damage_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    damage_level: Mapped[DamageLevel] = mapped_column(
        SQLEnum(DamageLevel),
        nullable=False
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
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

    ai_analysis: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )