from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Tạo "Động cơ" (Engine) kết nối tới SQL Server bằng URL lấy từ file .env
engine = create_engine(settings.DATABASE_URL)

# 2. Tạo một nhà máy sản xuất các "Phiên làm việc" (Session) với DB 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Tạo một Class cơ sở (Base). Các Model (bảng trong DB) sau này sẽ kế thừa từ class này.
Base = declarative_base()

# 4. Hàm cung cấp Session cho các API
def get_db():
    db = SessionLocal() # Tạo một phiên làm việc mới
    try:
        yield db
    finally:
        db.close()