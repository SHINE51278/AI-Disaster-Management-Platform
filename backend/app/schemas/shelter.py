from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.models.shelter import ShelterStatus


class ShelterCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    address: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    capacity: int = Field(ge=1)
    current_occupancy: int = Field(default=0, ge=0)
    contact_number: str | None = Field(default=None, max_length=20)
    status: ShelterStatus = ShelterStatus.OPEN

    @model_validator(mode="after")
    def validate_occupancy(self):
        if self.current_occupancy > self.capacity:
            raise ValueError(
                "current_occupancy cannot exceed capacity"
            )
        return self


class ShelterUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    address: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    capacity: int | None = Field(default=None, ge=1)
    current_occupancy: int | None = Field(default=None, ge=0)
    contact_number: str | None = Field(default=None, max_length=20)
    status: ShelterStatus | None = None


class ShelterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str | None
    latitude: float | None
    longitude: float | None
    capacity: int
    current_occupancy: int
    contact_number: str | None
    status: ShelterStatus
    created_at: datetime
    updated_at: datetime