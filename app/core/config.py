from pydantic_settings import BaseSettings  # Обновленный импорт

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    DATABASE_URL: str  # Убираем значение по умолчанию, оно будет загружаться из .env
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"  # Загрузка переменных из .env



# Инициализация объекта настроек
settings = Settings()
