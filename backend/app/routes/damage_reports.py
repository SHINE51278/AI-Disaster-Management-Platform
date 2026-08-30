from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.damage_report import DamageReport
from backend.app.models.incident import Incident
from backend.app.schemas.damage_report import (
    DamageReportCreate,
    DamageReportResponse,
    DamageReportUpdate,
)


router = APIRouter(
    prefix="/damage-reports",
    tags=["Damage Reports"],
)


@router.post(
    "",
    response_model=DamageReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_damage_report(
    report_data: DamageReportCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Verify that the referenced incident exists.
    incident = (
        db.query(Incident)
        .filter(
            Incident.id == report_data.incident_id
        )
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    report = DamageReport(
        incident_id=report_data.incident_id,
        image_url=report_data.image_url,
        damage_type=report_data.damage_type,
        damage_level=report_data.damage_level,
        confidence_score=report_data.confidence_score,
        latitude=report_data.latitude,
        longitude=report_data.longitude,
        ai_analysis=report_data.ai_analysis,
        verified=report_data.verified,
    )

    db.add(report)

    try:
        db.commit()
        db.refresh(report)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create damage report",
        )

    return report


@router.get(
    "",
    response_model=list[DamageReportResponse],
)
def get_damage_reports(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(DamageReport)
        .order_by(DamageReport.id.desc())
        .all()
    )


@router.get(
    "/{report_id}",
    response_model=DamageReportResponse,
)
def get_damage_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = (
        db.query(DamageReport)
        .filter(
            DamageReport.id == report_id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Damage report not found",
        )

    return report


@router.put(
    "/{report_id}",
    response_model=DamageReportResponse,
)
def update_damage_report(
    report_id: int,
    report_data: DamageReportUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    report = (
        db.query(DamageReport)
        .filter(
            DamageReport.id == report_id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Damage report not found",
        )

    update_data = report_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            report,
            field,
            value,
        )

    try:
        db.commit()
        db.refresh(report)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update damage report",
        )

    return report