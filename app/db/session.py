from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Загружаем переменные из файла .env
load_dotenv(encoding='utf-8')  # or try 'latin-1' if utf-8 doesn't work

# Получаем строку подключения из переменных окружения
DATABASE_URL ="postgresql://postgres:123123@localhost:5433/DB_BLOG"

# Если переменная окружения пустая, выводим ошибку
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)