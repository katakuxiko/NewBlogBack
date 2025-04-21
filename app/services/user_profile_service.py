# services/user_profile.py
from sqlalchemy.orm import Session
from app.db.repositories.user_profile_repo import UserProfileRepository
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate
from app.models.user_profile import UserProfile
from app.utils.minio_uploader import upload_base64_image

class UserProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, user_id: int) -> UserProfile:
        return UserProfileRepository.get_by_user_id(self.db, user_id)

    def update_profile(self, user_id: int, data: UserProfileUpdate) -> UserProfile:
        profile = self.get_profile(user_id)

        # Если пришла картинка, загружаем и подменяем avatar_url
        avatar_url = None
        if data.avatar_base64:
            avatar_url = upload_base64_image(data.avatar_base64)

        update_data = data.dict(exclude_unset=True, exclude={"avatar_base64"})
        if avatar_url:
            update_data["avatar_url"] = avatar_url

        if not profile:
            # Создаём профиль, если не существует
            profile_data = UserProfileCreate(**update_data)
            return self.create_profile(user_id, profile_data)

        # Обновляем существующий профиль
        return UserProfileRepository.update(self.db, profile, update_data)


    def delete_profile(self, user_id: int):
        profile = self.get_profile(user_id)
        if not profile:
            raise ValueError("Profile not found")
        UserProfileRepository.delete(self.db, profile)
    
    def create_profile(self, user_id: int, data: UserProfileCreate):
        avatar_url = None
        if data.avatar_base64:
            avatar_url = upload_base64_image(data.avatar_base64)
            
        profile_data = data.dict(exclude={"avatar_base64"})
        profile_data["avatar_url"] = avatar_url

        return UserProfileRepository.create(self.db, user_id, profile_data)
