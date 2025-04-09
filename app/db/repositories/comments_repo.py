from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comments import CommentCreate, CommentUpdate

# Создание комментария
def create_comment(db: Session, comment: CommentCreate, post_id: int, owner_id: int):
    db_comment = Comment(
        content=comment.content,
        post_id=post_id,
        owner_id=owner_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Получение комментария по ID
def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

# Получение всех комментариев для конкретного поста
def get_comments_for_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

# Обновление комментария
def update_comment(db: Session, comment_id: int, comment: CommentUpdate):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        if comment.content:
            db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)
    return db_comment

# Удаление комментария
def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
