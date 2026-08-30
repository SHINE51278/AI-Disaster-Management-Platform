from math import asin, cos, radians, sin, sqrt

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.hospital import Hospital, HospitalStatus
from backend.app.schemas.hospital import (
    HospitalCreate,
    HospitalResponse,
    HospitalUpdate,
)


router = APIRouter(
    prefix="/hospitals",
    tags=["Hospitals"],
)


def calculate_distance_km(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> float:
    """
    Calculate the distance between two coordinates
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
    response_model=HospitalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hospital(
    hospital_data: HospitalCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    hospital = Hospital(
        **hospital_data.model_dump()
    )

    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    return hospital


@router.get(
    "",
    response_model=list[HospitalResponse],
)
def get_hospitals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Hospital).all()


@router.get(
    "/nearby",
    response_model=list[HospitalResponse],
)
def get_nearby_hospitals(
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
    hospitals = (
        db.query(Hospital)
        .filter(
            Hospital.status == HospitalStatus.OPEN
        )
        .all()
    )

    nearby_hospitals = []

    for hospital in hospitals:

        if (
            hospital.latitude is None
            or hospital.longitude is None
        ):
            continue

        distance = calculate_distance_km(
            latitude,
            longitude,
            hospital.latitude,
            hospital.longitude,
        )

        if distance <= radius_km:
            nearby_hospitals.append(
                (distance, hospital)
            )

    nearby_hospitals.sort(
        key=lambda item: item[0]
    )

    return [
        hospital
        for distance, hospital in nearby_hospitals
    ]


@router.get(
    "/{hospital_id}",
    response_model=HospitalResponse,
)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    hospital = (
        db.query(Hospital)
        .filter(Hospital.id == hospital_id)
        .first()
    )

    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found",
        )

    return hospital


@router.put(
    "/{hospital_id}",
    response_model=HospitalResponse,
)
def update_hospital(
    hospital_id: int,
    hospital_data: HospitalUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    hospital = (
        db.query(Hospital)
        .filter(Hospital.id == hospital_id)
        .first()
    )

    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found",
        )

    update_data = hospital_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(hospital, field, value)

    db.commit()
    db.refresh(hospital)

    return hospital