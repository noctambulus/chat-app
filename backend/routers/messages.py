from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User, Message, RoomMember
from auth import get_current_user

router = APIRouter(prefix="/messages", tags=["messages"])


class SendMessageRequest(BaseModel):
    content: str
    room_id: int


def _require_membership(db: Session, user_id: int, room_id: int):
    member = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id, RoomMember.user_id == user_id)
        .first()
    )
    if member is None:
        raise HTTPException(status_code=403, detail="Not a member of this room")


@router.post("/", status_code=status.HTTP_201_CREATED)
def send_message(
    payload: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_membership(db, current_user.id, payload.room_id)

    message = Message(
        content=payload.content,
        sender_id=current_user.id,
        room_id=payload.room_id,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "id": message.id,
        "content": message.content,
        "sender_id": message.sender_id,
        "room_id": message.room_id,
        "created_at": message.created_at,
    }


@router.get("/{room_id}")
def get_messages(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_membership(db, current_user.id, room_id)

    messages = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return [
        {
            "id": m.id,
            "content": m.content,
            "sender_id": m.sender_id,
            "room_id": m.room_id,
            "created_at": m.created_at,
        }
        for m in messages
    ]
