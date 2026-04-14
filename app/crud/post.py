from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


# Hàm tạo bài viết mới
def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(title=post.title, content=post.content, owner_id = user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Hàm 2: Lấy danh sách bài viết (có phân trang skip, limit)
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).order_by(Post.id.desc()).offset(skip).limit(limit).all()

# Hàm 3: Lấy bài viết theo ID
def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

# Hàm 4: Cập nhật bài viết
def update_post(db: Session, db_post: Post, post_update: PostUpdate):
    # Chuyển dữ liệu schema thành dictionary, loại bỏ các trường bị null
    update_data = post_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_post, key, value) # Cập nhật từng trường vào Model
    
    db.commit()
    db.refresh(db_post)
    return db_post

# Hàm 5: Xóa bài viết
def delete_post(db: Session, db_post: Post):
    db.delete(db_post)
    db.commit()
    return True
