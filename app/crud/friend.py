from sqlalchemy.orm import Session
from app.models.friend import Friendship
from fastapi import HTTPException

# 1. Gửi lời mời kết bạn
def send_friend_request(db: Session, user_id: int, friend_id: int):
    # Kiểm tra: Không được tự kết bạn chính mình
    if user_id == friend_id:
        raise HTTPException(status_code=400, detail="Bạn không thể kết bạn với chính mình")

    # Kiểm tra: Đã có lời mời hoặc đã là bạn chưa (kiểm tra cả 2 chiều A-B và B-A)
    existing_request = db.query(Friendship).filter(
        ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id))
    ).first()

    if existing_request:
        raise HTTPException(status_code=400, detail="Lời mời đã tồn tại hoặc hai người đã là bạn")

    new_request = Friendship(user_id=user_id, friend_id=friend_id, status="pending")
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

# 2. Chấp nhận lời mời
def accept_friend_request(db: Session, request_id: int, current_user_id: int):
    db_request = db.query(Friendship).filter(Friendship.id == request_id).first()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Không tìm thấy lời mời kết bạn")
    
    # Chỉ người nhận lời mời mới có quyền chấp nhận
    if db_request.friend_id != current_user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền chấp nhận lời mời này")
    
    db_request.status = "accepted"
    db.commit()
    db.refresh(db_request)
    return db_request

# 3. Lấy danh sách bạn bè (những bản ghi có status là accepted)
def get_friends_list(db: Session, user_id: int):
    return db.query(Friendship).filter(
        ((Friendship.user_id == user_id) | (Friendship.friend_id == user_id)),
        Friendship.status == "accepted"
    ).all()