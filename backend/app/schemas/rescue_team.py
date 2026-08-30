from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.rescue_team import (
    RescueTeamStatus,
    RescueTeamType,
)


class RescueTeamCreate(BaseModel):
    team_name: str = Field(min_length=2, max_length=150)
    team_type: RescueTeamType
    status: RescueTeamStatus = RescueTeamStatus.AVAILABLE
    latitude: float | None = None
    longitude: float | None = None
    contact_number: str | None = Field(default=None, max_length=20)
    capacity: int = Field(ge=1)


class RescueTeamUpdate(BaseModel):
    team_name: str | None = Field(default=None, min_length=2, max_length=150)
    team_type: RescueTeamType | None = None
    status: RescueTeamStatus | None = None
    latitude: float | None = None
    longitude: float | None = None
    contact_number: str | None = Field(default=None, max_length=20)
    capacity: int | None = Field(default=None, ge=1)


class RescueTeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    team_name: str
    team_type: RescueTeamType
    status: RescueTeamStatus
    latitude: float | None
    longitude: float | None
    contact_number: str | None
    capacity: int
    created_at: datetime