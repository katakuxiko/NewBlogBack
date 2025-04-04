from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

def create_post(db: Session, post_data: PostCreate, user_id: int):
    new_post = Post(**post_data.dict(), owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_posts(db: Session):
    return db.query(Post).all()

def get_user_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.owner_id == user_id).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()
    if post:
        for key, value in post_data.dict().items():
            setattr(post, key, value)
        db.commit()
        db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post
