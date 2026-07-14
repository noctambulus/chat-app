from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt
from database import SessionLocal, User, RoomMember, Message
from auth import SECRET_KEY, ALGORITHM
from websocket import manager

router = APIRouter()


def _get_user_room_ids(db, user_id: int) -> List[int]:
    memberships = db.query(RoomMember).filter(RoomMember.user_id == user_id).all()
    return [m.room_id for m in memberships]


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, token: str = Query(...)):
    db = SessionLocal()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        await websocket.close(code=1008)
        db.close()
        return

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        await websocket.close(code=1008)
        db.close()
        return

    await manager.connect(websocket, room_id)

    user.is_online = True
    db.commit()
    await manager.broadcast_presence(user.id, True, _get_user_room_ids(db, user.id))

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")
            msg_room_id = data.get("room_id")

            member = (
                db.query(RoomMember)
                .filter(RoomMember.room_id == msg_room_id, RoomMember.user_id == user.id)
                .first()
            )
            if member is None:
                continue

            message = Message(content=content, sender_id=user.id, room_id=msg_room_id)
            db.add(message)
            db.commit()
            db.refresh(message)

            await manager.broadcast(
                {
                    "event": "message",
                    "id": message.id,
                    "content": message.content,
                    "sender_id": message.sender_id,
                    "room_id": message.room_id,
                    "created_at": message.created_at.isoformat(),
                },
                msg_room_id,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        user.is_online = False
        db.commit()
        await manager.broadcast_presence(user.id, False, _get_user_room_ids(db, user.id))
    finally:
        db.close()
