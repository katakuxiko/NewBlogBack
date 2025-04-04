from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.db.repositories import post_repo
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_repo.create_post(db, post, current_user.id)

@router.get("/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return post_repo.get_posts(db)

@router.get("/my", response_model=List[PostResponse])
def get_my_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_repo.get_user_posts(db, current_user.id)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_post = post_repo.update_post(db, post_id, post, current_user.id)
    if not updated_post:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return updated_post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_post = post_repo.delete_post(db, post_id, current_user.id)
    if not deleted_post:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    return {"message": "Post deleted"}
