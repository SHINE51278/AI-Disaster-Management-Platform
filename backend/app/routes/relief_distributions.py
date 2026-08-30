from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.relief_distribution import ReliefDistribution
from backend.app.schemas.relief_distribution import (
    ReliefDistributionCreate,
    ReliefDistributionResponse,
    ReliefDistributionUpdate,
)
from backend.app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/relief-distributions",
    tags=["Relief Distributions"],
)


@router.post(
    "",
    response_model=ReliefDistributionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_relief_distribution(
    distribution_data: ReliefDistributionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    distribution = ReliefDistribution(
        incident_id=distribution_data.incident_id,
        resource_id=distribution_data.resource_id,
        beneficiary_name=distribution_data.beneficiary_name,
        beneficiary_contact=distribution_data.beneficiary_contact,
        quantity=distribution_data.quantity,
        distributed_by=distribution_data.distributed_by,
        distribution_location=distribution_data.distribution_location,
        status=distribution_data.status,
    )

    db.add(distribution)

    try:
        db.commit()
        db.refresh(distribution)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create relief distribution",
        )

    return distribution


@router.get(
    "",
    response_model=list[ReliefDistributionResponse],
)
def get_relief_distributions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(ReliefDistribution).all()


@router.get(
    "/{distribution_id}",
    response_model=ReliefDistributionResponse,
)
def get_relief_distribution(
    distribution_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    distribution = (
        db.query(ReliefDistribution)
        .filter(ReliefDistribution.id == distribution_id)
        .first()
    )

    if not distribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relief distribution not found",
        )

    return distribution


@router.put(
    "/{distribution_id}",
    response_model=ReliefDistributionResponse,
)
def update_relief_distribution(
    distribution_id: int,
    distribution_data: ReliefDistributionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    distribution = (
        db.query(ReliefDistribution)
        .filter(ReliefDistribution.id == distribution_id)
        .first()
    )

    if not distribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relief distribution not found",
        )

    update_data = distribution_data.model_dump(exclude_unset=True)

    if (
        update_data.get("status")
        and update_data["status"].value == "DISTRIBUTED"
        and "distributed_at" not in update_data
    ):
        update_data["distributed_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(distribution, field, value)

    try:
        db.commit()
        db.refresh(distribution)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update relief distribution",
        )

    return distribution