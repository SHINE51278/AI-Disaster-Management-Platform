from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.relief_distribution import ReliefDistributionStatus


class ReliefDistributionCreate(BaseModel):
    incident_id: int
    resource_id: int
    beneficiary_name: str = Field(min_length=2, max_length=200)
    beneficiary_contact: str | None = Field(
        default=None,
        max_length=20
    )
    quantity: float = Field(gt=0)
    distributed_by: int
    distribution_location: str = Field(
        min_length=2,
        max_length=255
    )
    status: ReliefDistributionStatus = ReliefDistributionStatus.PLANNED


class ReliefDistributionUpdate(BaseModel):
    beneficiary_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )
    beneficiary_contact: str | None = Field(
        default=None,
        max_length=20
    )
    quantity: float | None = Field(default=None, gt=0)
    distribution_location: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )
    distributed_at: datetime | None = None
    status: ReliefDistributionStatus | None = None


class ReliefDistributionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    incident_id: int
    resource_id: int
    beneficiary_name: str
    beneficiary_contact: str | None
    quantity: float
    distributed_by: int
    distribution_location: str
    distributed_at: datetime | None
    status: ReliefDistributionStatus