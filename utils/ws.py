from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

class ConnectionManager:
    """"Clase Manejadora de conexiones."""
    def __init__(self):
        self.active_connections: Dict[int,list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: int):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: int):
        self.active_connections[game_id].remove(websocket)
        if not self.active_connections[game_id]:
            del self.active_connections[game_id]

    #async def send_personal_message(self, message: str, game_id: int, user_id: int):
    #    for connection in self.active_connections[game_id]:
    #        if connection[0] == user_id:
    #            await connection[1].send_text(message)

    async def broadcast(self, message: str, game_id: int):
        if game_id  in self.active_connections:
            for connection in self.active_connections[game_id]:
                await connection.send_text(message)

manager = ConnectionManager()