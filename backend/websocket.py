from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        connections = self.active_connections.get(room_id)
        if connections and websocket in connections:
            connections.remove(websocket)
            if not connections:
                del self.active_connections[room_id]

    async def broadcast(self, message: dict, room_id: int):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_json(message)

    async def broadcast_presence(self, user_id: int, is_online: bool, room_ids: List[int]):
        event = {"event": "presence", "user_id": user_id, "is_online": is_online}
        for room_id in room_ids:
            await self.broadcast(event, room_id)


manager = ConnectionManager()
