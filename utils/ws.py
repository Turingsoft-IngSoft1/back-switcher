from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    """Clase Manejadora de conexiones."""

    def __init__(self):
        self.active_connections: Dict[int, Dict[str, Dict[int, WebSocket]]] = {} #pragma: no cover

    async def connect(self, websocket: WebSocket, id_game: int, id_user: int, route: str = 'ws'): #pragma: no cover
        await websocket.accept() #pragma: no cover
        if id_game not in self.active_connections: #pragma: no cover
            self.active_connections[id_game] = {} #pragma: no cover
        if route not in self.active_connections[id_game]:
            self.active_connections[id_game][route] = {} #pragma: no cover
        self.active_connections[id_game][route][id_user] = websocket #pragma: no cover

    def disconnect(self, id_game: int, id_user: int, route: str = 'ws'): #pragma: no cover
        if self.active_connections[id_game]: #pragma: no cover
            if self.active_connections[id_game][route]: #pragma: no cover
                if self.active_connections[id_game][route][id_user]: #pragma: no cover
                    del self.active_connections[id_game][route][id_user] #pragma: no cover
            else:
                del self.active_connections[id_game][route] #pragma: no cover
        else:
            del self.active_connections[id_game] #pragma: no cover

    async def send_personal_message(self, message: str, id_game: int, id_user: int, route: str = 'ws'): #pragma: no cover
        if id_game in self.active_connections and route in self.active_connections[id_game]: #pragma: no cover
            for u in self.active_connections[id_game][route]: #pragma: no cover
                if u == id_user: #pragma: no cover
                    await self.active_connections[id_game][route][u].send_text(message) #pragma: no cover
                    break

    async def broadcast(self, message: str, id_game: int, route: str = 'ws'): #pragma: no cover
        if id_game in self.active_connections and route in self.active_connections[id_game]: #pragma: no cover
            for u in self.active_connections[id_game][route]: #pragma: no cover
                await self.active_connections[id_game][route][u].send_text(message) #pragma: no cover

manager = ConnectionManager() #pragma: no cover

def is_disconnected(id_game: int, id_user: int, m = manager.active_connections): #pragma: no cover
    return (m.get(id_game, {}).get('ws', {}).get(id_user) is None) #pragma: no cover