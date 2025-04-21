from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileOut
from app.services.user_profile_service import UserProfileService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/profiles", tags=["UserProfile"])

@router.get("/me", response_model=UserProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserProfileService(db)
    profile = service.get_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/", response_model=UserProfileOut)
def create_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserProfileService(db)
    existing = service.get_profile(current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return service.create_profile(current_user.id, profile_data)


@router.put("/", response_model=UserProfileOut)
def update_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserProfileService(db)
    try:
        return service.update_profile(current_user.id, profile_data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.delete("/")
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserProfileService(db)
    try:
        service.delete_profile(current_user.id)
        return {"detail": "Profile deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Profile not found")
