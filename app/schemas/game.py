from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DistractorResponse(BaseModel):
    id: int
    distractor_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class GameResponse(BaseModel):
    id: int
    title: str
    original_text: str
    host: Optional[str] = None
    category: Optional[str] = None
    grade_level: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    distractors: List[DistractorResponse] = []
    
    class Config:
        from_attributes = True

class GameCreateRequest(BaseModel):
    title: str
    original_text: str
    host: Optional[str] = None
    category: Optional[str] = None
    grade_level: Optional[int] = None
