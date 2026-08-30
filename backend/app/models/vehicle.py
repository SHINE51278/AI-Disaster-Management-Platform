from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class VehicleType(str, Enum):
    AMBULANCE = "AMBULANCE"
    FIRE_TRUCK = "FIRE_TRUCK"
    RESCUE_VEHICLE = "RESCUE_VEHICLE"
    BOAT = "BOAT"
    HELICOPTER = "HELICOPTER"
    OTHER = "OTHER"


class VehicleStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    ON_SITE = "ON_SITE"
    UNAVAILABLE = "UNAVAILABLE"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    vehicle_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    vehicle_type: Mapped[VehicleType] = mapped_column(
        SQLEnum(VehicleType),
        nullable=False
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("rescue_teams.id"),
        nullable=False
    )

    status: Mapped[VehicleStatus] = mapped_column(
        SQLEnum(VehicleStatus),
        nullable=False,
        default=VehicleStatus.AVAILABLE
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )