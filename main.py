from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from router import pre_game
from router.game import game
from router.cards import cards
from typing import List

from models.base import Base, engine

# TODO -> Agregar los import con los modelos implementados, esto crea la tabla en la base de datos.
from models.figure import FigureTable
from models.move import MoveTable


app = FastAPI(
    title="Switcher - TuringSoft™",
    description="Descripcion de prueba.",
    version="0.1.0",
)

origins = ["http://localhost:5173",
           "http://localhost:5174",
           "http://localhost:5175",
           "http://localhost:8000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pre_game)
app.include_router(game)
app.include_router(cards)

# Crea las tablas en base a los models importados.


Base.metadata.create_all(bind=engine)

class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

