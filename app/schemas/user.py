from pydantic import BaseModel, EmailStr

# 1. Schema cho dữ liệu người dùng gửi lên khi Đăng ký
class UserCreate(BaseModel):
    username: str
    email: EmailStr # Tự động kiểm tra xem có đúng chuẩn @gmail.com... không
    password: str

# 2. Schema cho dữ liệu API trả về cho người dùng xem
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True # Giúp Pydantic đọc được dữ liệu từ SQLAlchemy Model