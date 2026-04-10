import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

# Hàm mã hóa mật khẩu (Dùng khi Đăng ký)
def get_password_hash(password: str) -> str:
    # 1. bcrypt yêu cầu dữ liệu phải ở dạng byte (mã hóa utf-8)
    password_bytes = password.encode('utf-8')
    
    # 2. Tạo một chuỗi ngẫu nhiên (salt) để cộng gộp vào mật khẩu cho an toàn hơn
    salt = bcrypt.gensalt()
    
    # 3. Băm mật khẩu
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Giải mã ngược lại thành chuỗi văn bản (string) để lưu được vào SQL Server
    return hashed_password_bytes.decode('utf-8')

# Hàm kiểm tra mật khẩu (Dùng cho lúc Đăng nhập sau này)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Chuyển cả mật khẩu người dùng nhập và mật khẩu trong DB ra dạng byte để so sánh
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

# Hàm tạo Access Token (JWT) sau khi người dùng đăng nhập thành công
def create_access_token(data: dict, expires_delta: timedelta = None):
    # Sao chép dữ liệu gốc để thêm thông tin thời gian hết hạn vào token
    to_encode = data.copy()
    
    # Tính thời gian hết hạn cho token (mặc định là 30 phút nếu không có expires_delta)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Thêm thông tin thời gian hết hạn vào payload của token
    to_encode.update({"exp": expire})
    
    # Sử dụng thư viện JWT để tạo token (cần cài thêm thư viện PyJWT)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

