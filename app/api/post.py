from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # Dùng để khai báo kiểu dữ liệu là một Danh sách (List)

from app.db.database import get_db
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.crud import post as crud_post
from app.api.user import get_current_user # Import hàm "soát vé" từ api user
from app.models.user import User

# Khởi tạo Router cho Post
router = APIRouter(prefix="/posts", tags=["Posts"])

# 1. API Tạo bài viết (BẮT BUỘC ĐĂNG NHẬP)
@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Hệ thống tự động chặn nếu không có Token hợp lệ
):
    # Lấy ID của user đang đăng nhập truyền xuống cho Database
    return crud_post.create_post(db=db, post=post, user_id=current_user.id)

# 2. API Lấy danh sách bài viết (KHÔNG YÊU CẦU ĐĂNG NHẬP)
@router.get("/", response_model=List[PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud_post.get_posts(db, skip=skip, limit=limit)
    return posts

# 3. API Lấy chi tiết bài viết theo ID
@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    return db_post

# 4. API Cập nhật bài viết (BẮT BUỘC ĐĂNG NHẬP, CHỈ CHỦ SỞ HỮU MỚI CÓ QUYỀN SỬA)
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền sửa bài viết này")

    return crud_post.update_post(db=db, db_post=db_post, post_update=post)    

# 5. API Xóa bài viết (BẮT BUỘC ĐĂNG NHẬP, CHỈ CHỦ SỞ HỮU MỚI CÓ QUYỀN XÓA)`    
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = crud_post.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Bài viết không tồn tại")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa bài viết này")

    crud_post.delete_post(db=db, db_post=db_post)
    return {"message": "Bài viết đã được xóa thành công"}
