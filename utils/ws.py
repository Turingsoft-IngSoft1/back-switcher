from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Tuple

class ConnectionManager:
    """"Clase Manejadora de conexiones."""
    def __init__(self):
        self.active_connections: Dict[int, list[Tuple [int,WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, game_id: int, user_id: int):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append((user_id, websocket))

    def disconnect(self, websocket: WebSocket, game_id: int, user_id: int):
        self.active_connections[game_id].remove((user_id, websocket))
        if not self.active_connections[game_id]:
            del self.active_connections[game_id]

    async def send_personal_message(self, message: str, game_id: int, user_id: int):
        if game_id in self.active_connections:
            for uid, ws in self.active_connections[game_id]:
                if uid == user_id:
                    await ws.send_text(message)
                    break

    async def broadcast(self, message: str, game_id: int):
        if game_id  in self.active_connections:
            for _,ws in self.active_connections[game_id]:
                await ws.send_text(message)

manager = ConnectionManager()