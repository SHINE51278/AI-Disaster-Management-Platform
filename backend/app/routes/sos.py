from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.sos import SOSRequest, SOSStatus
from backend.app.models.user import User
from backend.app.schemas.sos import SOSCreate, SOSResponse


router = APIRouter(
    prefix="/sos",
    tags=["SOS"]
)


@router.post(
    "",
    response_model=SOSResponse,
    status_code=status.HTTP_201_CREATED
)
def create_sos(
    sos_data: SOSCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_sos = SOSRequest(
        user_id=current_user.id,
        incident_id=sos_data.incident_id,
        emergency_type=sos_data.emergency_type,
        people_count=sos_data.people_count,
        latitude=sos_data.latitude,
        longitude=sos_data.longitude
    )

    db.add(new_sos)
    db.commit()
    db.refresh(new_sos)

    return new_sos


@router.get(
    "/active",
    response_model=list[SOSResponse]
)
def get_active_sos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    active_statuses = [
        SOSStatus.RECEIVED,
        SOSStatus.PRIORITIZED,
        SOSStatus.ASSIGNED,
        SOSStatus.RESCUE_IN_PROGRESS,
    ]

    sos_requests = (
        db.query(SOSRequest)
        .filter(SOSRequest.status.in_(active_statuses))
        .order_by(
            SOSRequest.priority_score.desc(),
            SOSRequest.created_at.asc()
        )
        .all()
    )

    return sos_requests


@router.get(
    "/{sos_id}",
    response_model=SOSResponse
)
def get_sos(
    sos_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sos_request = (
        db.query(SOSRequest)
        .filter(SOSRequest.id == sos_id)
        .first()
    )

    if sos_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SOS request not found"
        )

    return sos_request