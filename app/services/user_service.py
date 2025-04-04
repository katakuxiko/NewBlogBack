from sqlalchemy.orm import Session
from app.db.repositories.user_repo import get_user_by_username, create_user
from app.schemas.user import UserCreate
from fastapi import HTTPException

def register_user(db: Session, user_data: UserCreate):
    """
    Регистрирует нового пользователя
    """
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return create_user(db, user_data)

def authenticate_user(db: Session, username: str, password: str, verify_password):
    """
    Проверяет учетные данные пользователя
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
