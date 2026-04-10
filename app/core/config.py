import os
from dotenv import load_dotenv

# Tải các biến từ file .env vào hệ thống
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Các cài đặt khác liên quan đến bảo mật, JWT, v.v... có thể thêm vào đây
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key") # Mặc định nếu không có trong .env
    ALGORITHM = os.getenv("ALGORITHM", "HS256") # Mặc định nếu không có trong .env
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) # Mặc định là 30 phút nếu không có trong .env

# Khởi tạo một object settings để các file khác gọi dùng
settings = Settings()