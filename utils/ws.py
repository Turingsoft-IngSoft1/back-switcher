from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    """Clase Manejadora de conexiones."""

    def __init__(self):
        self.active_connections: Dict[int, Dict[str, list[tuple[int, WebSocket]]]] = {} #pragma: no cover

    async def connect(self, websocket: WebSocket, id_game: int, id_user: int, route: str = 'ws'):
        await websocket.accept() #pragma: no cover
        if id_game not in self.active_connections: #pragma: no cover
            self.active_connections[id_game] = {} #pragma: no cover
        if route not in self.active_connections[id_game]: #pragma: no cover
            self.active_connections[id_game][route] = [] #pragma: no cover
        self.active_connections[id_game][route].append((id_user, websocket)) #pragma: no cover

    def disconnect(self, websocket: WebSocket, id_game: int, id_user: int, route: str = 'ws'):
        self.active_connections[id_game][route].remove((id_user, websocket)) #pragma: no cover
        if not self.active_connections[id_game][route]: #pragma: no cover
            del self.active_connections[id_game][route] #pragma: no cover
        if not self.active_connections[id_game]: #pragma: no cover
            del self.active_connections[id_game] #pragma: no cover

    async def send_personal_message(self, message: str, id_game: int, id_user: int, route: str = 'ws'):
        if id_game in self.active_connections and route in self.active_connections[id_game]: #pragma: no cover
            for uid, ws in self.active_connections[id_game][route]: #pragma: no cover
                if uid == id_user: #pragma: no cover
                    await ws.send_text(message) #pragma: no cover
                    break

    async def broadcast(self, message: str, id_game: int, route: str = 'ws'):
        if id_game in self.active_connections and route in self.active_connections[id_game]: #pragma: no cover
            for _, ws in self.active_connections[id_game][route]: #pragma: no cover
                await ws.send_text(message) #pragma: no cover

manager = ConnectionManager()
