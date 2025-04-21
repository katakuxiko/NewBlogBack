# repositories/user_profile.py
from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate

class UserProfileRepository:
    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> UserProfile:
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    @staticmethod
    def create(db: Session, user_id: int, profile_data: UserProfileCreate) -> UserProfile:
        profile = UserProfile(user_id=user_id, **profile_data)  # ✅
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update(db: Session, profile: UserProfile, updates: UserProfileUpdate) -> UserProfile:
        for field, value in updates.items():  # ✅
            setattr(profile, field, value)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def delete(db: Session, profile: UserProfile):
        db.delete(profile)
        db.commit()
