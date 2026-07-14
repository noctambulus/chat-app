from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User, Room, RoomMember
from auth import get_current_user

router = APIRouter(prefix="/channels", tags=["channels"])


class CreateRoomRequest(BaseModel):
    name: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_room(
    payload: CreateRoomRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = Room(name=payload.name, is_dm=False)
    db.add(room)
    db.commit()
    db.refresh(room)

    db.add(RoomMember(user_id=current_user.id, room_id=room.id))
    db.commit()

    return {"id": room.id, "name": room.name, "is_dm": room.is_dm}


@router.get("/")
def list_rooms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rooms = (
        db.query(Room)
        .join(RoomMember, RoomMember.room_id == Room.id)
        .filter(RoomMember.user_id == current_user.id)
        .all()
    )
    return [{"id": r.id, "name": r.name, "is_dm": r.is_dm} for r in rooms]


@router.post("/{room_id}/join", status_code=status.HTTP_201_CREATED)
def join_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    existing = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id, RoomMember.user_id == current_user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already a member of this room")

    db.add(RoomMember(user_id=current_user.id, room_id=room_id))
    db.commit()

    return {"id": room.id, "name": room.name, "is_dm": room.is_dm}


@router.post("/dm/{target_user_id}", status_code=status.HTTP_201_CREATED)
def create_dm(
    target_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target_user = db.query(User).filter(User.id == target_user_id).first()
    if target_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_ids = sorted([current_user.id, target_user.id])
    room = Room(name=f"dm_{user_ids[0]}_{user_ids[1]}", is_dm=True)
    db.add(room)
    db.commit()
    db.refresh(room)

    db.add_all([
        RoomMember(user_id=user_ids[0], room_id=room.id),
        RoomMember(user_id=user_ids[1], room_id=room.id),
    ])
    db.commit()

    return {"id": room.id, "name": room.name, "is_dm": room.is_dm}
