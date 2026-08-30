from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.road_blockage import (
    BlockageType,
    BlockageStatus,
)
from backend.app.models.incident import IncidentSeverity


class RoadBlockageCreate(BaseModel):
    road_name: str = Field(min_length=2, max_length=255)
    blockage_type: BlockageType
    severity: IncidentSeverity
    geometry: dict[str, Any]
    reported_by: int
    status: BlockageStatus = BlockageStatus.ACTIVE


class RoadBlockageUpdate(BaseModel):
    road_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )
    blockage_type: BlockageType | None = None
    severity: IncidentSeverity | None = None
    geometry: dict[str, Any] | None = None
    status: BlockageStatus | None = None


class RoadBlockageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    road_name: str
    blockage_type: BlockageType
    severity: IncidentSeverity
    geometry: dict[str, Any]
    reported_by: int
    status: BlockageStatus
    created_at: datetime
    updated_at: datetime