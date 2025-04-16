from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.utils.minio_uploader import upload_base64_image
from app.utils.elasticsearch_client import es
from elasticsearch.exceptions import ElasticsearchWarning


INDEX_NAME = "posts"

# Индексируем пост в Elasticsearch
def index_post(post: Post):
    document = {
        "title": post.title,
        "content": post.content,
        "tags": post.tags,
        "created_at": post.created_at,
        "approval_status": post.approval_status,
        "post_status": post.post_status,
        "image_url": post.image_url,
        "owner_id": post.owner_id,
    }
    es.index(index=INDEX_NAME, id=post.id, document=document)

def update_post_in_elasticsearch(post: Post):
    document = {
        "title": post.title,
        "content": post.content,
        "tags": post.tags,
        "created_at": post.created_at,
        "approval_status": post.approval_status,
        "post_status": post.post_status,
        "image_url": post.image_url,
        "owner_id": post.owner_id,

    }
    es.index(index=INDEX_NAME, id=post.id, document=document)

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

    index_post(db_post)


    return db_post

def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int) -> Optional[Post]:
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()

    if post_data.image_base64:
        post.image_url = upload_base64_image(post_data.image_base64)
    if not post:
        return None

    for key, value in post_data.dict(exclude_unset=True).items():
        setattr(post, key, value)
    post.approval_status = "pending"
    db.commit()
    db.refresh(post)

    update_post_in_elasticsearch(post)

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

def search_posts(query: str, approval_status: Optional[str] = None, post_status: Optional[str] = None, tags: Optional[str] = None) -> List[dict]:
    # Создаем список обязательных запросов (must queries)
    must_queries = [
        {"multi_match": {
            "query": query,
            "fields": ["title^3", "content^2", "tags"]
        },}
    ]

    # Добавляем дополнительные фильтры по статусам
    filter_queries = []

    if approval_status:
        filter_queries.append({"term": {"approval_status": approval_status}})
    if post_status:
        filter_queries.append({"term": {"post_status": post_status}})
    if tags:
        # Если переданы теги, делаем поиск через match или terms, если предполагаются несколько тегов
        filter_queries.append({"match": {"tags": tags}})

    # Формируем запрос
    body = {
        "query": {
            "bool": {
                "must": must_queries,
                "filter": filter_queries  # Используем фильтрацию для точных значений
            }
        }
    }

    try:
        # Выполняем запрос в Elasticsearch
        result = es.search(index="posts", body=body)
        
        # Формируем и возвращаем список с обязательными полями
        posts = []
        for hit in result["hits"]["hits"]:
            post = hit["_source"]
            # Добавляем обязательные поля, если их нет в данных
            post["id"] = hit["_id"]
            post["owner_id"] = hit["_source"].get("owner_id", None)  # Если поле owner_id не в Elasticsearch, подставляем None
            posts.append(post)
        
        return posts
    
    except ElasticsearchWarning as e:
        # Обработка ошибки Elasticsearch
        print(f"Error executing search query: {e}")
        return []
