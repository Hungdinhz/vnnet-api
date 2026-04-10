from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship # Thêm dòng này
from app.db.database import Base

class User(Base):
    __tablename__ = "users" # Tên bảng sẽ xuất hiện trong SQL Server

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Thiết lập mối quan hệ 2 chiều với Model Post
    posts = relationship("Post", back_populates="owner")
    