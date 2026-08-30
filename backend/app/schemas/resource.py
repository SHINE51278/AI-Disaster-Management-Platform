from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.resource import (
    ResourceType,
    ResourceStatus,
)


class ResourceCreate(BaseModel):
    resource_type: ResourceType
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=50)
    location: str | None = Field(
        default=None,
        max_length=255
    )
    status: ResourceStatus = ResourceStatus.AVAILABLE


class ResourceUpdate(BaseModel):
    resource_type: ResourceType | None = None
    quantity: float | None = Field(
        default=None,
        gt=0
    )
    unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    location: str | None = Field(
        default=None,
        max_length=255
    )
    status: ResourceStatus | None = None


class ResourceAllocate(BaseModel):
    resource_id: int = Field(gt=0)
    quantity: float = Field(gt=0)


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resource_type: ResourceType
    quantity: float
    unit: str
    location: str | None
    status: ResourceStatus
    created_at: datetime
    updated_at: datetime