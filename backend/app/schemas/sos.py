from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.sos import SOSStatus


class SOSCreate(BaseModel):
    incident_id: int | None = None
    emergency_type: str = Field(min_length=2, max_length=100)
    people_count: int = Field(default=1, ge=1)
    latitude: float | None = None
    longitude: float | None = None

class SOSUpdate(BaseModel):
    incident_id: int | None = None
    priority_score: int | None = Field(default=None, ge=0, le=100)
    status: SOSStatus | None = None
    resolved_at: datetime | None = None


class SOSResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    incident_id: int | None
    emergency_type: str
    people_count: int
    latitude: float | None
    longitude: float | None
    priority_score: int
    status: SOSStatus
    created_at: datetime
    resolved_at: datetime | None