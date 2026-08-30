from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2 import Geography
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape, mapping
from sqlalchemy import cast, func
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.risk_zone import RiskZone
from backend.app.schemas.risk_zone import (
    RiskZoneCreate,
    RiskZoneResponse,
    RiskZoneUpdate,
)


router = APIRouter(
    prefix="/risk-zones",
    tags=["Risk Zones"],
)


def risk_zone_response(risk_zone: RiskZone):
    return {
        "id": risk_zone.id,
        "disaster_type": risk_zone.disaster_type,
        "risk_score": risk_zone.risk_score,
        "risk_level": risk_zone.risk_level,
        "geometry": mapping(
            to_shape(risk_zone.geometry)
        ),
        "valid_from": risk_zone.valid_from,
        "valid_until": risk_zone.valid_until,
        "created_at": risk_zone.created_at,
    }


@router.post(
    "",
    response_model=RiskZoneResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_risk_zone(
    risk_data: RiskZoneCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        geometry = shape(risk_data.geometry)

        if geometry.geom_type != "Polygon":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="geometry must be a Polygon",
            )

        risk_zone = RiskZone(
            disaster_type=risk_data.disaster_type,
            risk_score=risk_data.risk_score,
            risk_level=risk_data.risk_level,
            geometry=from_shape(
                geometry,
                srid=4326,
            ),
            valid_from=risk_data.valid_from,
            valid_until=risk_data.valid_until,
        )

        db.add(risk_zone)
        db.commit()
        db.refresh(risk_zone)

        return risk_zone_response(risk_zone)

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
    response_model=list[RiskZoneResponse],
)
def get_risk_zones(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    risk_zones = db.query(RiskZone).all()

    return [
        risk_zone_response(risk_zone)
        for risk_zone in risk_zones
    ]


@router.get(
    "/nearby",
    response_model=list[RiskZoneResponse],
)
def get_nearby_risk_zones(
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
    point = func.ST_SetSRID(
        func.ST_MakePoint(
            longitude,
            latitude,
        ),
        4326,
    )

    point_geography = cast(
        point,
        Geography(
            geometry_type="POINT",
            srid=4326,
        ),
    )

    geometry_geography = cast(
        RiskZone.geometry,
        Geography(
            geometry_type="POLYGON",
            srid=4326,
        ),
    )

    radius_meters = radius_km * 1000

    now = datetime.utcnow()

    risk_zones = (
        db.query(RiskZone)
        .filter(
            func.ST_DWithin(
                geometry_geography,
                point_geography,
                radius_meters,
            )
        )
        .filter(
            RiskZone.valid_from <= now
        )
        .filter(
            (RiskZone.valid_until.is_(None))
            | (RiskZone.valid_until >= now)
        )
        .all()
    )

    return [
        risk_zone_response(risk_zone)
        for risk_zone in risk_zones
    ]


@router.get(
    "/{risk_zone_id}",
    response_model=RiskZoneResponse,
)
def get_risk_zone(
    risk_zone_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    risk_zone = (
        db.query(RiskZone)
        .filter(
            RiskZone.id == risk_zone_id
        )
        .first()
    )

    if not risk_zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found",
        )

    return risk_zone_response(risk_zone)


@router.put(
    "/{risk_zone_id}",
    response_model=RiskZoneResponse,
)
def update_risk_zone(
    risk_zone_id: int,
    risk_data: RiskZoneUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    risk_zone = (
        db.query(RiskZone)
        .filter(
            RiskZone.id == risk_zone_id
        )
        .first()
    )

    if not risk_zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk zone not found",
        )

    update_data = risk_data.model_dump(
        exclude_unset=True
    )

    if "geometry" in update_data:
        geometry = shape(
            update_data["geometry"]
        )

        if geometry.geom_type != "Polygon":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="geometry must be a Polygon",
            )

        update_data["geometry"] = from_shape(
            geometry,
            srid=4326,
        )

    for field, value in update_data.items():
        setattr(
            risk_zone,
            field,
            value,
        )

    db.commit()
    db.refresh(risk_zone)

    return risk_zone_response(risk_zone)