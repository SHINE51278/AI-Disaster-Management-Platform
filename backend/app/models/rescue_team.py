from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class RescueTeamType(str, Enum):
    MEDICAL = "MEDICAL"
    FIRE = "FIRE"
    POLICE = "POLICE"
    FLOOD_RESCUE = "FLOOD_RESCUE"
    GENERAL_RESCUE = "GENERAL_RESCUE"


class RescueTeamStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    ON_SITE = "ON_SITE"
    UNAVAILABLE = "UNAVAILABLE"


class RescueTeam(Base):
    __tablename__ = "rescue_teams"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    team_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    team_type: Mapped[RescueTeamType] = mapped_column(
        SQLEnum(RescueTeamType),
        nullable=False
    )

    status: Mapped[RescueTeamStatus] = mapped_column(
        SQLEnum(RescueTeamStatus),
        nullable=False,
        default=RescueTeamStatus.AVAILABLE
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    contact_number: Mapped[str | None] = mapped_column(
        String(20),
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