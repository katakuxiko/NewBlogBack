from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, posts, comments, user_profile
from app.db.base import Base
from app.models import user, post, comment  # Импорт всех моделей для регистрации
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlowPassword

app = FastAPI(
    title="FastAPI Backend",
    description="Backend с авторизацией Bearer Token",
    version="1.0.0",
	
)

Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)  # Удаляем все таблицы при запуске приложения

# Добавляем CORS, если нужно
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(user_profile.router, prefix="/api/v1/user_profile", tags=["user_profile"])

