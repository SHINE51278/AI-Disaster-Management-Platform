from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.models.hospital import HospitalStatus


class HospitalCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    address: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    emergency_capacity: int = Field(ge=1)
    available_beds: int = Field(ge=0)
    contact_number: str | None = Field(default=None, max_length=20)
    status: HospitalStatus = HospitalStatus.OPEN

    @model_validator(mode="after")
    def validate_beds(self):
        if self.available_beds > self.emergency_capacity:
            raise ValueError(
                "available_beds cannot exceed emergency_capacity"
            )
        return self


class HospitalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=200)
    address: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None
    emergency_capacity: int | None = Field(default=None, ge=1)
    available_beds: int | None = Field(default=None, ge=0)
    contact_number: str | None = Field(default=None, max_length=20)
    status: HospitalStatus | None = None


class HospitalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str | None
    latitude: float | None
    longitude: float | None
    emergency_capacity: int
    available_beds: int
    contact_number: str | None
    status: HospitalStatus
    created_at: datetime
    updated_at: datetime