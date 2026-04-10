from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    # Khóa ngoại trỏ đến cột id của bảng users
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Thiết lập mối quan hệ 2 chiều với Model User
    owner = relationship("User", back_populates="posts")