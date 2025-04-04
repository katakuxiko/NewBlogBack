from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.repositories.user_repo import create_user, get_user_by_username
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

# Функция для получения базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Обработчик POST запроса для создания пользователя
@router.post("/users/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким же именем
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Создаём пользователя
    return create_user(db, user)
