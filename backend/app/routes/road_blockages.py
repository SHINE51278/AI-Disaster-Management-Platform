from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2 import Geography
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import mapping, shape
from sqlalchemy import cast, func
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.road_blockage import (
    BlockageStatus,
    RoadBlockage,
)
from backend.app.schemas.road_blockage import (
    RoadBlockageCreate,
    RoadBlockageResponse,
    RoadBlockageUpdate,
)


router = APIRouter(
    prefix="/road-blockages",
    tags=["Road Blockages"],
)


def road_blockage_response(
    blockage: RoadBlockage,
):
    return {
        "id": blockage.id,
        "road_name": blockage.road_name,
        "blockage_type": blockage.blockage_type,
        "severity": blockage.severity,
        "geometry": mapping(
            to_shape(blockage.geometry)
        ),
        "reported_by": blockage.reported_by,
        "status": blockage.status,
        "created_at": blockage.created_at,
        "updated_at": blockage.updated_at,
    }


@router.post(
    "",
    response_model=RoadBlockageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_road_blockage(
    blockage_data: RoadBlockageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        geometry = shape(
            blockage_data.geometry
        )

        if geometry.geom_type != "LineString":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="geometry must be a LineString",
            )

        blockage = RoadBlockage(
            road_name=blockage_data.road_name,
            blockage_type=blockage_data.blockage_type,
            severity=blockage_data.severity,
            geometry=from_shape(
                geometry,
                srid=4326,
            ),
            reported_by=blockage_data.reported_by,
            status=blockage_data.status,
        )

        db.add(blockage)
        db.commit()
        db.refresh(blockage)

        return road_blockage_response(
            blockage
        )

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid geometry: {str(e)}",
        )


@router.get(
    "",
    response_model=list[RoadBlockageResponse],
)
def get_road_blockages(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    blockages = (
        db.query(RoadBlockage)
        .all()
    )

    return [
        road_blockage_response(blockage)
        for blockage in blockages
    ]


@router.get(
    "/nearby",
    response_model=list[RoadBlockageResponse],
)
def get_nearby_road_blockages(
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
    # Create a PostGIS point using
    # longitude first, then latitude.
    point = func.ST_SetSRID(
        func.ST_MakePoint(
            longitude,
            latitude,
        ),
        4326,
    )

    # Convert the point to geography so that
    # ST_DWithin uses meters.
    point_geography = cast(
        point,
        Geography(
            geometry_type="POINT",
            srid=4326,
        ),
    )

    # Convert the road LINESTRING to geography.
    geometry_geography = cast(
        RoadBlockage.geometry,
        Geography(
            geometry_type="LINESTRING",
            srid=4326,
        ),
    )

    radius_meters = radius_km * 1000

    blockages = (
        db.query(RoadBlockage)
        .filter(
            RoadBlockage.status
            == BlockageStatus.ACTIVE
        )
        .filter(
            func.ST_DWithin(
                geometry_geography,
                point_geography,
                radius_meters,
            )
        )
        .all()
    )

    return [
        road_blockage_response(blockage)
        for blockage in blockages
    ]


@router.get(
    "/{blockage_id}",
    response_model=RoadBlockageResponse,
)
def get_road_blockage(
    blockage_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    blockage = (
        db.query(RoadBlockage)
        .filter(
            RoadBlockage.id == blockage_id
        )
        .first()
    )

    if not blockage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Road blockage not found",
        )

    return road_blockage_response(
        blockage
    )


@router.put(
    "/{blockage_id}",
    response_model=RoadBlockageResponse,
)
def update_road_blockage(
    blockage_id: int,
    blockage_data: RoadBlockageUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    blockage = (
        db.query(RoadBlockage)
        .filter(
            RoadBlockage.id == blockage_id
        )
        .first()
    )

    if not blockage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Road blockage not found",
        )

    update_data = blockage_data.model_dump(
        exclude_unset=True
    )

    if "geometry" in update_data:
        geometry = shape(
            update_data["geometry"]
        )

        if geometry.geom_type != "LineString":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="geometry must be a LineString",
            )

        update_data["geometry"] = from_shape(
            geometry,
            srid=4326,
        )

    for field, value in update_data.items():
        setattr(
            blockage,
            field,
            value,
        )

    db.commit()
    db.refresh(blockage)

    return road_blockage_response(
        blockage
    )