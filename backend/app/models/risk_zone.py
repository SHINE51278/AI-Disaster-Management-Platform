from datetime import datetime
from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Enum as SQLEnum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base
from backend.app.models.incident import DisasterType


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskZone(Base):
    __tablename__ = "risk_zones"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    disaster_type: Mapped[DisasterType] = mapped_column(
        SQLEnum(DisasterType),
        nullable=False
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    risk_level: Mapped[RiskLevel] = mapped_column(
        SQLEnum(RiskLevel),
        nullable=False
    )

    geometry = mapped_column(
        Geometry(
            geometry_type="POLYGON",
            srid=4326
        ),
        nullable=False
    )

    valid_from: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    valid_until: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )