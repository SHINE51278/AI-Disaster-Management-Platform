from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.vehicle import (
    VehicleType,
    VehicleStatus,
)


class VehicleCreate(BaseModel):
    vehicle_number: str = Field(min_length=2, max_length=50)
    vehicle_type: VehicleType
    team_id: int
    status: VehicleStatus = VehicleStatus.AVAILABLE
    latitude: float | None = None
    longitude: float | None = None
    capacity: int = Field(ge=1)


class VehicleUpdate(BaseModel):
    vehicle_number: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    vehicle_type: VehicleType | None = None
    team_id: int | None = None
    status: VehicleStatus | None = None
    latitude: float | None = None
    longitude: float | None = None
    capacity: int | None = Field(default=None, ge=1)


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_number: str
    vehicle_type: VehicleType
    team_id: int
    status: VehicleStatus
    latitude: float | None
    longitude: float | None
    capacity: int
    created_at: datetime