from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    birthday: Optional[str] = Field(None)
    address: Optional[str] = Field(None, max_length=500)


class UserProfileResponse(BaseModel):
    """Schema for user profile response."""
    id: int
    email: str
    full_name: Optional[str]
    phone: Optional[str]
    birthday: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True


@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile information."""
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=getattr(current_user, 'phone', None),
        birthday=getattr(current_user, 'birthday', None),
        address=getattr(current_user, 'address', None)
    )


@router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile information."""

    # Update only provided fields
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.birthday is not None:
        current_user.birthday = profile_data.birthday
    if profile_data.address is not None:
        current_user.address = profile_data.address

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        birthday=current_user.birthday,
        address=current_user.address
    )
