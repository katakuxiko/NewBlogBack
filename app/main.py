from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, posts
from app.db.base import Base
from app.models import user, post  # Импорт всех моделей для регистрации
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import OAuthFlowPassword

app = FastAPI(
    title="FastAPI Backend",
    description="Backend с авторизацией Bearer Token",
    version="1.0.0",
	
)

# Создаём таблицы по всем моделям
Base.metadata.create_all(bind=engine)

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

