from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.incident import Incident, IncidentStatus
from backend.app.models.user import User
from backend.app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatusUpdate,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_incident(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        disaster_type=incident_data.disaster_type,
        severity=incident_data.severity,
        priority_score=incident_data.priority_score,
        latitude=incident_data.latitude,
        longitude=incident_data.longitude,
        reported_by=current_user.id
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get(
    "/active",
    response_model=list[IncidentResponse]
)
def get_active_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    active_statuses = [
        IncidentStatus.REPORTED,
        IncidentStatus.VERIFIED,
        IncidentStatus.ASSIGNED,
        IncidentStatus.IN_PROGRESS,
    ]

    incidents = (
        db.query(Incident)
        .filter(Incident.status.in_(active_statuses))
        .order_by(Incident.priority_score.desc())
        .all()
    )

    return incidents


@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse
)
def update_incident_status(
    incident_id: int,
    status_data: IncidentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )

    incident.status = status_data.status

    db.commit()
    db.refresh(incident)

    return incident


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )

    return incident