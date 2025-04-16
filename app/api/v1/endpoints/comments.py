from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.comments import CommentInDB, CommentCreate, CommentUpdate, CommentResponse
from app.services.comments_service import CommentService
from app.api.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter()

# Создание комментария
@router.post("/", response_model=CommentInDB)
def create_comment(
    comment: CommentCreate,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_service = CommentService(db)
    db_comment = comment_service.create(comment, post_id, current_user.id)
    return db_comment

# Получение всех комментариев для поста
@router.get("/posts/{post_id}/", response_model=list[CommentResponse])
def get_comments_for_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    comment_service = CommentService(db)
    return comment_service.get_for_post(post_id, skip, limit)

# Получение одного комментария по ID
@router.get("/{comment_id}", response_model=CommentInDB)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    db_comment = comment_service.get(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.put("/{comment_id}", response_model=CommentInDB)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_service = CommentService(db)
    db_comment = comment_service.get(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to update this comment")

    updated_comment = comment_service.update(comment_id, comment)
    return updated_comment

@router.delete("/{comment_id}", response_model=CommentInDB)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_service = CommentService(db)
    db_comment = comment_service.get(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this comment")

    deleted_comment = comment_service.delete(comment_id)
    return deleted_comment

