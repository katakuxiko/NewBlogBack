from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional

class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None
    post_status: Optional[str] = "draft"  # можно также использовать Literal или Enum

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    approval_status: Optional[str] = None
    post_status: Optional[str] = None
    tags: Optional[str] = None

class PostResponse(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    approved_at: Optional[datetime] = None
    approval_status: str
    post_status: str

    class Config:
        from_attributes = True

class PostModerationUpdate(BaseModel):
    approval_status: Literal["approved", "rejected"]