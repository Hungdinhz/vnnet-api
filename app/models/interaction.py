from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from app.db.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    # Ràng buộc: Một user chỉ được phép Like một post ĐÚNG 1 LẦN
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)