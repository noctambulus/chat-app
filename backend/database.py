"""
# @ Author: Abdallah - Copyright © 2026 Abdallah
# @ Creation Date: 2026-06-24 22:47:36 CT
# @ Last Modification Date: 2026-06-24 23:32:33 CT
# @ Modified by: Abdallah
# @ Description:
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./chat.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_online = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="sender")
    memberships = relationship("RoomMember", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_dm = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="room")
    members = relationship("RoomMember", back_populates="room")


class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="memberships")
    room = relationship("Room", back_populates="members")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)