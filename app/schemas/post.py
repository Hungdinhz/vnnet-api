from pydantic import BaseModel
from typing import Optional

# 1. Schema cho dữ liệu người dùng gửi lên khi tạo bài viết
class PostBase(BaseModel):
    title: str
    content: str

# 2. Schema cho dữ liệu người dùng gửi lên khi tạo bài viết (có thể thêm các trường khác nếu cần)
class PostCreate(PostBase):
    pass

# Schema cho việc cập nhật bài viết
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# 3. Schema cho dữ liệu API trả về cho người dùng xem
class PostResponse(PostBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True # Giúp Pydantic đọc được dữ liệu từ SQLAlchemy Model

