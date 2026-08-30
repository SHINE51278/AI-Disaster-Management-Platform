from datetime import datetime
from enum import Enum

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class BlockageType(str, Enum):
    FLOOD = "FLOOD"
    DEBRIS = "DEBRIS"
    COLLAPSE = "COLLAPSE"
    FIRE = "FIRE"
    TRAFFIC = "TRAFFIC"
    OTHER = "OTHER"


class BlockageStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLEARED = "CLEARED"
    UNKNOWN = "UNKNOWN"


class RoadBlockage(Base):
    __tablename__ = "road_blockages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    road_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    blockage_type: Mapped[BlockageType] = mapped_column(
        SQLEnum(BlockageType),
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    geometry = mapped_column(
        Geometry(
            geometry_type="LINESTRING",
            srid=4326
        ),
        nullable=False
    )

    reported_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    status: Mapped[BlockageStatus] = mapped_column(
        SQLEnum(BlockageStatus),
        nullable=False,
        default=BlockageStatus.ACTIVE
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