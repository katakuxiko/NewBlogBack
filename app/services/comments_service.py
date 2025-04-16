from sqlalchemy.orm import Session
from app.db.repositories.comments_repo import create_comment, get_comment, get_comments_for_post, update_comment, delete_comment
from app.schemas.comments import CommentCreate, CommentUpdate
from app.db.repositories.user_repo import get_user_by_id

class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: CommentCreate, post_id: int, owner_id: int):
        return create_comment(self.db, comment, post_id, owner_id)

    def get(self, comment_id: int):
        return get_comment(self.db, comment_id)

    def get_for_post(self, post_id: int, skip: int = 0, limit: int = 100):
        comments = get_comments_for_post(self.db, post_id, skip, limit)
        for comment in comments:
            comment.owner_username = self._get_owner_username(comment.owner_id)
        return comments

    def _get_owner_username(self, owner_id: int):
        user = get_user_by_id(self.db, owner_id)
        return user.username if user else None

    def update(self, comment_id: int, comment: CommentUpdate):
        return update_comment(self.db, comment_id, comment)

    def delete(self, comment_id: int):
        return delete_comment(self.db, comment_id)