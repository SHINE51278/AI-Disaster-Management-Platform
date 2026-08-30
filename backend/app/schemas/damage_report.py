from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.damage_report import DamageLevel


class DamageReportCreate(BaseModel):
    incident_id: int
    image_url: str | None = Field(default=None, max_length=500)
    damage_type: str | None = Field(default=None, max_length=100)
    damage_level: DamageLevel
    confidence_score: float | None = Field(
        default=None,
        ge=0,
        le=100
    )
    latitude: float | None = None
    longitude: float | None = None
    ai_analysis: str | None = None
    verified: bool = False


class DamageReportUpdate(BaseModel):
    damage_type: str | None = Field(default=None, max_length=100)
    damage_level: DamageLevel | None = None
    confidence_score: float | None = Field(
        default=None,
        ge=0,
        le=100
    )
    latitude: float | None = None
    longitude: float | None = None
    ai_analysis: str | None = None
    verified: bool | None = None


class DamageReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    incident_id: int
    image_url: str | None
    damage_type: str | None
    damage_level: DamageLevel
    confidence_score: float | None
    latitude: float | None
    longitude: float | None
    ai_analysis: str | None
    verified: bool
    created_at: datetime