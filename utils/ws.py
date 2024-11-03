from typing import Dict, Tuple

from fastapi import WebSocket


class ConnectionManager:
    """"Clase Manejadora de conexiones."""

    def __init__(self):
        self.active_connections: Dict[int, list[Tuple[int, WebSocket]]] = {}  #pragma: no cover

    async def connect(self, websocket: WebSocket, id_game: int, id_user: int):
        await websocket.accept()  #pragma: no cover
        if id_game not in self.active_connections:
            self.active_connections[id_game] = []  #pragma: no cover
        self.active_connections[id_game].append((id_user, websocket))  #pragma: no cover

    def disconnect(self, websocket: WebSocket, id_game: int, id_user: int):
        self.active_connections[id_game].remove((id_user, websocket))  #pragma: no cover
        if not self.active_connections[id_game]:  #pragma: no cover
            del self.active_connections[id_game]  #pragma: no cover

    async def send_personal_message(self, message: str, id_game: int, id_user: int):
        if id_game in self.active_connections:
            for uid, ws in self.active_connections[id_game]:
                if uid == id_user:
                    await ws.send_text(message)  #pragma: no cover
                    break

    async def broadcast(self, message: str, id_game: int):
        if id_game in self.active_connections:
            for _, ws in self.active_connections[id_game]:
                await ws.send_text(message)  #pragma: no cover


manager = ConnectionManager()
