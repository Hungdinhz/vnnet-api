from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user # Import để SQLAlchemy nhận diện được Model User

# Lệnh này sẽ yêu cầu SQLAlchemy kiểm tra DB, nếu chưa có bảng thì tự động tạo!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Social Network API",
    description="API cho mạng xã hội thu nhỏ",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Xin chào Hùng, Server FastAPI đã chạy thành công!"}