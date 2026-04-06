import os
from dotenv import load_dotenv

# Tải các biến từ file .env vào hệ thống
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

# Khởi tạo một object settings để các file khác gọi dùng
settings = Settings()