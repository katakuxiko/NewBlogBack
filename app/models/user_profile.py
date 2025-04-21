from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)  # Краткая информация о себе
    interests = Column(Text, nullable=True)  # Интересы, например: "Python, чтение, путешествия"
    location = Column(String, nullable=True)  # Местоположение, например: "Алматы, Казахстан"

    user = relationship("User", back_populates="profile")
