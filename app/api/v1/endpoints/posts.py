from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import SessionLocal
from app.db.repositories import post_repo
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostModerationUpdate
from app.api.deps import get_current_user
from app.models.user import Role, User
from app.api.deps import get_db
from app.db.repositories.post_repo import search_posts

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_repo.create_post(db, post, current_user.id)

@router.get("/", response_model=List[PostResponse])
def get_all_posts(
    db: Session = Depends(get_db),
    approval_status: Optional[str] = Query(None),
    post_status: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
):
    return post_repo.get_posts(
        db,
        approval_status=approval_status,
        post_status=post_status,
        owner_id=owner_id,
        title=title
    )

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

@router.patch("/moderate/{post_id}", response_model=PostResponse)
def moderate_post(
    post_id: int,
    moderation: PostModerationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print('ROLE', current_user.username, current_user.role)
    if current_user.role not in [Role.ADMIN, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Access denied")

    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.approval_status = moderation.approval_status
    post.approved_at = datetime.now() if moderation.approval_status == "approved" else None

    db.commit()
    db.refresh(post)
    return post

@router.get("/search/post", response_model=List[PostResponse])
def search(
    query: str,
    approval_status: Optional[str] = Query(None, enum=["pending", "approved", "rejected"]),
    post_status: Optional[str] = Query(None, enum=["draft", "published", "archived"]),
    tags: Optional[str] = None
):
    # Выполняем поиск через Elasticsearch
    results = search_posts(query, approval_status, post_status, tags)

    return results