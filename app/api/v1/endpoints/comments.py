from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import services
from app.db.session import SessionLocal
from app.schemas.comments import CommentInDB, CommentCreate, CommentUpdate
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание комментария
@router.post("/comments/", response_model=CommentInDB)
def create_comment(
    comment: CommentCreate,
    post_id: int,
    owner_id: int,
    db: Session = Depends(get_db)
):
    comment_service = services.CommentService(db)
    db_comment = comment_service.create(comment, post_id, owner_id)
    return db_comment

# Получение всех комментариев для поста
@router.get("/posts/{post_id}/comments/", response_model=list[CommentInDB])
def get_comments_for_post(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    comment_service = services.CommentService(db)
    return comment_service.get_for_post(post_id, skip, limit)

# Получение одного комментария по ID
@router.get("/comments/{comment_id}", response_model=CommentInDB)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_service = services.CommentService(db)
    db_comment = comment_service.get(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

# Обновление комментария
@router.put("/comments/{comment_id}", response_model=CommentInDB)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db)
):
    comment_service = services.CommentService(db)
    db_comment = comment_service.update(comment_id, comment)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

# Удаление комментария
@router.delete("/comments/{comment_id}", response_model=CommentInDB)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_service = services.CommentService(db)
    db_comment = comment_service.delete(comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment
