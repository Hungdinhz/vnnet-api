from fastapi import FastAPI

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Mini Social Network API",
    description="API cho mạng xã hội thu nhỏ",
    version="1.0.0"
)

# Tạo một route (đường dẫn) đơn giản để test
@app.get("/")
def read_root():
    return {"message": "Xin chào Hùng, Server FastAPI đã chạy thành công!"}