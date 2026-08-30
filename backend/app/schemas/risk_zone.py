from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.incident import DisasterType
from backend.app.models.risk_zone import RiskLevel


class RiskZoneCreate(BaseModel):
    disaster_type: DisasterType
    risk_score: float = Field(ge=0, le=100)
    risk_level: RiskLevel
    geometry: dict[str, Any]
    valid_from: datetime
    valid_until: datetime | None = None


class RiskZoneUpdate(BaseModel):
    disaster_type: DisasterType | None = None
    risk_score: float | None = Field(default=None, ge=0, le=100)
    risk_level: RiskLevel | None = None
    geometry: dict[str, Any] | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None


class RiskZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    disaster_type: DisasterType
    risk_score: float
    risk_level: RiskLevel
    geometry: dict[str, Any]
    valid_from: datetime
    valid_until: datetime | None
    created_at: datetime