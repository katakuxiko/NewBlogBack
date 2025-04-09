from typing import Optional
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.utils.minio_uploader import upload_base64_image

def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    image_url = None
    if post.image_base64:
        image_url = upload_base64_image(post.image_base64)

    db_post = Post(
        title=post.title,
        content=post.content,
        tags=post.tags,
        post_status=post.post_status,
        owner_id=user_id,
        image_url=image_url,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()
    if not post:
        return None

    for key, value in post_data.dict(exclude_unset=True).items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


def get_posts(
    db: Session,
    approval_status: Optional[str] = None,
    post_status: Optional[str] = None,
    owner_id: Optional[int] = None,
    title: Optional[str] = None,
):
    query = db.query(Post)

    if approval_status:
        query = query.filter(Post.approval_status == approval_status)
    if post_status:
        query = query.filter(Post.post_status == post_status)
    if owner_id:
        query = query.filter(Post.owner_id == owner_id)
    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))

    return query.order_by(Post.created_at.desc()).all()


def get_user_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.owner_id == user_id).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post
