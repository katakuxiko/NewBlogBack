from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    content: Optional[str] = None

class CommentInDB(CommentBase):
    id: int
    post_id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CommentResponse(CommentBase):
    id: int
    post_id: int
    owner_id: int
    created_at: datetime
    owner_username: Optional[str] = None
    class Config:
        orm_mode = True
