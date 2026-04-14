from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.user import get_current_user
from app.models.user import User
from app.schemas.friend import FriendshipResponse
from app.crud import friend as crud_friend

router = APIRouter(prefix="/friends", tags=["Friends"])

# API: Gửi lời mời kết bạn
@router.post("/request/{friend_id}", response_model=FriendshipResponse)
def send_request(friend_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_friend.send_friend_request(db, user_id=current_user.id, friend_id=friend_id)

# API: Chấp nhận lời mời (truyền ID của lời mời)
@router.post("/accept/{request_id}", response_model=FriendshipResponse)
def accept_request(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_friend.accept_friend_request(db, request_id=request_id, current_user_id=current_user.id)

# API: Xem danh sách bạn bè
@router.get("/list", response_model=List[FriendshipResponse])
def get_friends(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_friend.get_friends_list(db, user_id=current_user.id)