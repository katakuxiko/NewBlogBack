from sqlalchemy.orm import Session
from app.crud import create_comment, get_comment, get_comments_for_post, update_comment, delete_comment
from app.schemas import CommentCreate, CommentUpdate

class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: CommentCreate, post_id: int, owner_id: int):
        return create_comment(self.db, comment, post_id, owner_id)

    def get(self, comment_id: int):
        return get_comment(self.db, comment_id)

    def get_for_post(self, post_id: int, skip: int = 0, limit: int = 100):
        return get_comments_for_post(self.db, post_id, skip, limit)

    def update(self, comment_id: int, comment: CommentUpdate):
        return update_comment(self.db, comment_id, comment)

    def delete(self, comment_id: int):
        return delete_comment(self.db, comment_id)
