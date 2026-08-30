from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.rescue_team import RescueTeam
from backend.app.schemas.rescue_team import (
    RescueTeamCreate,
    RescueTeamResponse,
    RescueTeamUpdate,
)
from backend.app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/rescue-teams",
    tags=["Rescue Teams"],
)


@router.post(
    "",
    response_model=RescueTeamResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rescue_team(
    team_data: RescueTeamCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = RescueTeam(**team_data.model_dump())

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


@router.get(
    "",
    response_model=list[RescueTeamResponse],
)
def get_rescue_teams(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(RescueTeam).all()


@router.get(
    "/{team_id}",
    response_model=RescueTeamResponse,
)
def get_rescue_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = (
        db.query(RescueTeam)
        .filter(RescueTeam.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rescue team not found",
        )

    return team


@router.put(
    "/{team_id}",
    response_model=RescueTeamResponse,
)
def update_rescue_team(
    team_id: int,
    team_data: RescueTeamUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    team = (
        db.query(RescueTeam)
        .filter(RescueTeam.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rescue team not found",
        )

    update_data = team_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(team, field, value)

    db.commit()
    db.refresh(team)

    return team