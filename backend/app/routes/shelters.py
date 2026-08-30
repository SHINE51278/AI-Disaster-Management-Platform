from math import asin, cos, radians, sin, sqrt

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.shelter import Shelter, ShelterStatus
from backend.app.schemas.shelter import (
    ShelterCreate,
    ShelterResponse,
    ShelterUpdate,
)


router = APIRouter(
    prefix="/shelters",
    tags=["Shelters"],
)


def calculate_distance_km(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> float:
    """
    Calculate distance between two geographic coordinates
    using the Haversine formula.
    """

    earth_radius_km = 6371.0

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    delta_lat = radians(latitude2 - latitude1)
    delta_lon = radians(longitude2 - longitude1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return earth_radius_km * c


@router.post(
    "",
    response_model=ShelterResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shelter(
    shelter_data: ShelterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    shelter = Shelter(**shelter_data.model_dump())

    db.add(shelter)
    db.commit()
    db.refresh(shelter)

    return shelter


@router.get(
    "",
    response_model=list[ShelterResponse],
)
def get_shelters(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Shelter).all()


@router.get(
    "/nearby",
    response_model=list[ShelterResponse],
)
def get_nearby_shelters(
    latitude: float = Query(
        ...,
        ge=-90,
        le=90,
        description="User latitude",
    ),
    longitude: float = Query(
        ...,
        ge=-180,
        le=180,
        description="User longitude",
    ),
    radius_km: float = Query(
        default=10.0,
        gt=0,
        le=100,
        description="Search radius in kilometers",
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    shelters = (
        db.query(Shelter)
        .filter(
            Shelter.status.in_(
                [
                    ShelterStatus.OPEN,
                    ShelterStatus.EMERGENCY_ONLY,
                ]
            )
        )
        .all()
    )

    nearby_shelters = []

    for shelter in shelters:

        if shelter.latitude is None or shelter.longitude is None:
            continue

        distance = calculate_distance_km(
            latitude,
            longitude,
            shelter.latitude,
            shelter.longitude,
        )

        if distance <= radius_km:
            nearby_shelters.append(
                (distance, shelter)
            )

    nearby_shelters.sort(
        key=lambda item: item[0]
    )

    return [
        shelter
        for distance, shelter in nearby_shelters
    ]


@router.get(
    "/{shelter_id}",
    response_model=ShelterResponse,
)
def get_shelter(
    shelter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    shelter = (
        db.query(Shelter)
        .filter(Shelter.id == shelter_id)
        .first()
    )

    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shelter not found",
        )

    return shelter


@router.put(
    "/{shelter_id}",
    response_model=ShelterResponse,
)
def update_shelter(
    shelter_id: int,
    shelter_data: ShelterUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    shelter = (
        db.query(Shelter)
        .filter(Shelter.id == shelter_id)
        .first()
    )

    if not shelter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shelter not found",
        )

    update_data = shelter_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(shelter, field, value)

    db.commit()
    db.refresh(shelter)

    return shelter