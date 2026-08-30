from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.jwt import create_access_token
from backend.app.core.security import hash_password, verify_password
from backend.app.database.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserLogin

from backend.app.schemas.auth import (
    RegisterResponse,
    LoginResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def public_user_id(user_id: int) -> str:
    """
    Convert internal database ID into the public API user ID format
    defined by the API contract.
    
    Example:
        1 -> USR-0001
        25 -> USR-0025
    """
    return f"USR-{user_id:04d}"


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    # Check whether the email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Hash password before storing it
    hashed_password = hash_password(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hashed_password,
        role=user_data.role,
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not register user",
        )

    return {
        "success": True,
        "data": {
            "user_id": public_user_id(new_user.id),
        },
        "message": "Registration successful",
    }


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    # User does not exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate JWT access token
    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "user": {
                "id": public_user_id(user.id),
                "name": user.name,
                "role": user.role.value,
            },
        },
        "message": "Login successful",
    }