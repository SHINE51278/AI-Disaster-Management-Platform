from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.database import Base


class ResourceType(str, Enum):
    FOOD = "FOOD"
    WATER = "WATER"
    MEDICINE = "MEDICINE"
    CLOTHING = "CLOTHING"
    TENT = "TENT"
    BLANKET = "BLANKET"
    FUEL = "FUEL"
    OTHER = "OTHER"


class ResourceStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    resource_type: Mapped[ResourceType] = mapped_column(
        SQLEnum(ResourceType),
        nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[ResourceStatus] = mapped_column(
        SQLEnum(ResourceStatus),
        nullable=False,
        default=ResourceStatus.AVAILABLE
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