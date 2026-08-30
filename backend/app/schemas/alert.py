from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.alert import AlertType
from backend.app.models.incident import IncidentSeverity


class AlertCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=3)
    alert_type: AlertType
    severity: IncidentSeverity
    target_area: str | None = Field(default=None, max_length=255)
    created_by: int


class AlertUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    message: str | None = Field(default=None, min_length=3)
    alert_type: AlertType | None = None
    severity: IncidentSeverity | None = None
    target_area: str | None = Field(default=None, max_length=255)
    expires_at: datetime | None = None


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    message: str
    alert_type: AlertType
    severity: IncidentSeverity
    target_area: str | None
    created_by: int
    created_at: datetime
    expires_at: datetime | None