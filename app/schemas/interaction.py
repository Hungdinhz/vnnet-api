from pydantic import BaseModel

# Dùng khi user gửi nội dung bình luận lên
class CommentCreate(BaseModel):
    content: str

# Dùng khi API trả dữ liệu bình luận về
class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    class Config:
        from_attributes = True