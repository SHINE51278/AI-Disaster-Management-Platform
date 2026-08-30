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


class ReliefDistributionStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_TRANSIT = "IN_TRANSIT"
    DISTRIBUTED = "DISTRIBUTED"
    CANCELLED = "CANCELLED"


class ReliefDistribution(Base):
    __tablename__ = "relief_distributions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False
    )

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id"),
        nullable=False
    )

    beneficiary_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    beneficiary_contact: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    distributed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    distribution_location: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    distributed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[ReliefDistributionStatus] = mapped_column(
        SQLEnum(ReliefDistributionStatus),
        nullable=False,
        default=ReliefDistributionStatus.PLANNED
    )