from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.alert import Alert
from backend.app.schemas.alert import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)
from backend.app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    alert = Alert(
        title=alert_data.title,
        message=alert_data.message,
        alert_type=alert_data.alert_type,
        severity=alert_data.severity,
        target_area=alert_data.target_area,
        created_by=alert_data.created_by,
    )

    db.add(alert)

    try:
        db.commit()
        db.refresh(alert)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create alert",
        )

    return alert


@router.get(
    "",
    response_model=list[AlertResponse],
)
def get_alerts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Alert).all()


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert


@router.put(
    "/{alert_id}",
    response_model=AlertResponse,
)
def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    update_data = alert_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(alert, field, value)

    try:
        db.commit()
        db.refresh(alert)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update alert",
        )

    return alert