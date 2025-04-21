# schemas/user_profile.py
from pydantic import BaseModel, HttpUrl
from typing import Optional

class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    interests: Optional[str] = None
    location: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    avatar_base64: Optional[str] = None  # <-- для приёма base64


class UserProfileUpdate(UserProfileBase):
    avatar_url: Optional[HttpUrl] = None  # <-- здесь мы обновляем уже по url
    avatar_base64: Optional[str] = None  # 🔧 Добавить временно, не сохраняется в БД

class UserProfileOut(UserProfileBase):
    id: int
    user_id: int
    avatar_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True
