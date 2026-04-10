from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

# Hàm 1: Kiểm tra xem email này đã có ai dùng chưa
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Hàm 2: Tạo User mới
def create_user(db: Session, user: UserCreate):
    # 1. Băm mật khẩu người dùng gửi lên
    hashed_password = get_password_hash(user.password)
    
    # 2. Tạo một bản ghi Model User mới
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    # 3. Thêm vào Database và lưu lại (commit)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Cập nhật lại db_user để lấy cái ID vừa được SQL Server tự tạo
    
    return db_user

# Hàm 3: Xác thực người dùng (Dùng cho lúc Đăng nhập)
def authenticate_user(db: Session, email: str, password: str):
    # 1. Kiểm tra xem email này có tồn tại trong DB không
    user = get_user_by_email(db, email)
    if not user:
        return False

    # 2. Kiểm tra xem mật khẩu có đúng không
    if not verify_password(password, user.hashed_password):
        return False

    return user