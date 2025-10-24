from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    original_text = Column(Text, nullable=False)
    host = Column(String(100), nullable=True)
    category = Column(String(50), nullable=True)
    grade_level = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to distractors
    distractors = relationship("Distractor", back_populates="game", cascade="all, delete-orphan")
