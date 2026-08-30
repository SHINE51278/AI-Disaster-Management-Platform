from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.incident import (
    DisasterType,
    IncidentSeverity,
    IncidentStatus,
)


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    disaster_type: DisasterType
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    priority_score: int = Field(default=0, ge=0, le=100)
    latitude: float | None = None
    longitude: float | None = None


class IncidentUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=200
    )
    description: str | None = None
    disaster_type: DisasterType | None = None
    severity: IncidentSeverity | None = None
    priority_score: int | None = Field(
        default=None,
        ge=0,
        le=100
    )
    status: IncidentStatus | None = None
    latitude: float | None = None
    longitude: float | None = None


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    disaster_type: DisasterType
    severity: IncidentSeverity
    priority_score: int
    status: IncidentStatus
    latitude: float | None
    longitude: float | None
    reported_by: int
    created_at: datetime
    updated_at: datetime