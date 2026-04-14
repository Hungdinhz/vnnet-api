from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from app.db.database import Base

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    
    # Khóa ngoại đều trỏ về bảng users
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)   # Người gửi
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Người nhận
    
    # Trạng thái mặc định là pending (chờ duyệt)
    status = Column(String(20), default="pending", nullable=False) 

    # Ràng buộc: A chỉ có thể gửi 1 lời mời cho B (tránh spam click)
    __table_args__ = (UniqueConstraint('user_id', 'friend_id', name='_user_friend_uc'),)