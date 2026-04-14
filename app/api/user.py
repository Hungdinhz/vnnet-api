from fastapi import APIRouter, Depends, HTTPException,  status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user
from app.core.security import create_access_token
from app.schemas.token import Token
from app.core.config import settings

# Khai báo cấu hình bảo mật: Khai báo cho Swagger UI biết đường dẫn lấy token là ở đâu
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Tạo một "trạm trung chuyển" (router) quản lý các API của User
router = APIRouter(prefix="/users", tags=["Users"])

# API Đăng ký: Nhận vào UserCreate, Trả ra UserResponse (giấu password)
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Kiểm tra email trùng lặp
    db_user = crud_user.get_user_by_email(db, email=user.email)
    # Kiểm tra username trùng lặp
    db_user_username = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email này đã được đăng ký!")
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username này đã được sử dụng!")
    
    # 2. Gọi CRUD để lưu user
    return crud_user.create_user(db=db, user=user)

# API Đăng nhập: Nhận vào email + password, Trả ra Access Token nếu thành công
@router.post("/login", response_model=Token)
# API Đăng nhập: Trả về Token
@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username mặc định của FastAPI, nhưng hệ thống mình sẽ nhập email vào đó
    user = crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai email hoặc mật khẩu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Nếu đăng nhập đúng, tạo token có chứa email của user đó
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Hàm soát vé: Nhận vào token, giải mã xem có đúng không, nếu đúng thì lấy thông tin User từ DB
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin (Token không hợp lệ hoặc đã hết hạn)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Giải mã token bằng chìa khóa bí mật
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Lấy thông tin user từ DB
    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user

# API Lấy thông tin tài khoản đang đăng nhập (Bắt buộc phải có Token)
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_user)):
    # Trả về thẳng thông tin user, FastAPI sẽ tự động dùng UserResponse để lọc bỏ password
    return current_user





