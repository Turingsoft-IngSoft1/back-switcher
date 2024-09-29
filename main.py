from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from router.pre_game import pre_game
from router.game import game
from router.cards import cards

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

from utils.ws import manager
#manager.connect(websocket=WebSocket,game_id=1,user_id=1)
print(manager.active_connections)