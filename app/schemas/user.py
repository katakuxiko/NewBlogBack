from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str  # Добавили роли

    class Config:
        from_attributes = True
