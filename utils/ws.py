from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    """Clase Manejadora de conexiones."""

    def __init__(self):
        self.active_connections: Dict[int, Dict[str, list[tuple[int, WebSocket]]]] = {}

    async def connect(self, websocket: WebSocket, id_game: int, id_user: int, route: str = 'ws'):
        await websocket.accept()
        if id_game not in self.active_connections:
            self.active_connections[id_game] = {}
        if route not in self.active_connections[id_game]:
            self.active_connections[id_game][route] = []
        self.active_connections[id_game][route].append((id_user, websocket))

    def disconnect(self, websocket: WebSocket, id_game: int, id_user: int, route: str = 'ws'):
        self.active_connections[id_game][route].remove((id_user, websocket))
        if not self.active_connections[id_game][route]:
            del self.active_connections[id_game][route]
        if not self.active_connections[id_game]:
            del self.active_connections[id_game]

    async def send_personal_message(self, message: str, id_game: int, id_user: int, route: str = 'ws'):
        if id_game in self.active_connections and route in self.active_connections[id_game]:
            for uid, ws in self.active_connections[id_game][route]:
                if uid == id_user:
                    await ws.send_text(message)
                    break

    async def broadcast(self, message: str, id_game: int, route: str = 'ws'):
        if id_game in self.active_connections and route in self.active_connections[id_game]:
            for _, ws in self.active_connections[id_game][route]:
                await ws.send_text(message)

manager = ConnectionManager()
