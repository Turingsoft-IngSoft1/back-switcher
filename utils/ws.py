from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    """Clase Manejadora de conexiones."""

    def __init__(self):
        self.active_connections: Dict[int, Dict[str, Dict[int, WebSocket]]] = {} #pragma: no cover

    async def connect(self, websocket: WebSocket, id_game: int, id_user: int, route: str = 'ws'):
        await websocket.accept() #pragma: no cover
        if id_game not in self.active_connections:
            self.active_connections[id_game] = {} #pragma: no cover
        if route not in self.active_connections[id_game]:
            self.active_connections[id_game][route] = {} #pragma: no cover
        self.active_connections[id_game][route][id_user] = websocket #pragma: no cover

    def disconnect(self, id_game: int, id_user: int, route: str = 'ws'):
        if self.active_connections[id_game]: 
            if self.active_connections[id_game][route]:
                if self.active_connections[id_game][route][id_user]:
                    del self.active_connections[id_game][route][id_user] #pragma: no cover
            else:
                del self.active_connections[id_game][route] #pragma: no cover
        else:
            del self.active_connections[id_game] #pragma: no cover

    async def send_personal_message(self, message: str, id_game: int, id_user: int, route: str = 'ws'):
        if id_game in self.active_connections and route in self.active_connections[id_game]:
            for u in self.active_connections[id_game][route]: #pragma: no cover
                if u == id_user:
                    await self.active_connections[id_game][route][u].send_text(message) #pragma: no cover
                    break

    async def broadcast(self, message: str, id_game: int, route: str = 'ws'):
        if id_game in self.active_connections and route in self.active_connections[id_game]:
            for u in self.active_connections[id_game][route]:
                await self.active_connections[id_game][route][u].send_text(message) #pragma: no cover
    
    def is_currently_connected(self, id_game: int, id_user: int) -> bool:
        if self.active_connections[id_game]['ws'][id_user]: #pragma: no cover
            return True #pragma: no cover
        else:
            return False #pragma: no cover

manager = ConnectionManager()
