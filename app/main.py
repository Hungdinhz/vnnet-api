from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user, post # Import để SQLAlchemy nhận diện được Model User
from app.api import user as user_api, post as post_api # Import router của User và Post

# Lệnh này sẽ yêu cầu SQLAlchemy kiểm tra DB, nếu chưa có bảng thì tự động tạo!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Social Network API",
    description="API cho mạng xã hội thu nhỏ",
    version="1.0.0"
)

# Nhúng router của User vào ứng dụng
app.include_router(user_api.router)
# Nhúng router của Post vào ứng dụng
app.include_router(post_api.router)

@app.get("/")
def read_root():
    return {"message": "Xin chào Hùng, Server FastAPI đã chạy thành công!"}