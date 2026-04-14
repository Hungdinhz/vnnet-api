from sqlalchemy.orm import Session
from app.models.interaction import Like, Comment
from app.schemas.interaction import CommentCreate

# --- PHẦN XỬ LÝ LIKE ---

# Kiểm tra xem user đã like post này chưa
def get_like(db: Session, user_id: int, post_id: int):
    return db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()

# Tính năng Toggle Like (Thích / Bỏ thích)
def toggle_like(db: Session, user_id: int, post_id: int):
    existing_like = get_like(db, user_id, post_id)
    
    if existing_like:
        # Nếu đã like rồi thì xóa đi (Hủy like)
        db.delete(existing_like)
        db.commit()
        return {"message": "Đã hủy Like bài viết"}
    else:
        # Nếu chưa like thì tạo mới
        new_like = Like(user_id=user_id, post_id=post_id)
        db.add(new_like)
        db.commit()
        return {"message": "Đã Like bài viết thành công"}

# --- PHẦN XỬ LÝ COMMENT ---

# Thêm bình luận mới
def create_comment(db: Session, comment: CommentCreate, user_id: int, post_id: int):
    new_comment = Comment(
        content=comment.content, 
        user_id=user_id, 
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Lấy danh sách bình luận của 1 bài viết
def get_comments_by_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()