from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.resource import (
    Resource,
    ResourceStatus,
)
from backend.app.schemas.resource import (
    ResourceAllocate,
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)


router = APIRouter(
    prefix="/resources",
    tags=["Resources"],
)


@router.post(
    "",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    resource = Resource(
        **resource_data.model_dump()
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


@router.get(
    "",
    response_model=list[ResourceResponse],
)
def get_resources(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Resource).all()


@router.post(
    "/allocate",
    response_model=ResourceResponse,
)
def allocate_resource(
    allocation_data: ResourceAllocate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == allocation_data.resource_id)
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    if resource.status == ResourceStatus.OUT_OF_STOCK:
         raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Resource is out of stock",
    )
    if resource.quantity < allocation_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient resource quantity",
        )

    resource.quantity -= allocation_data.quantity

    if resource.quantity == 0:
        resource.status = ResourceStatus.OUT_OF_STOCK
    else:
        resource.status = ResourceStatus.RESERVED

    db.commit()
    db.refresh(resource)

    return resource


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    return resource


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse,
)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    update_data = resource_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(resource, field, value)

    db.commit()
    db.refresh(resource)

    return resource