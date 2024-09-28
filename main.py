from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.pre_game import pre_game
from router.game import game
from router.cards import cards

from models.base import Base, engine

from tests import move_queries, figure_queries, gameCreation

# TODO -> Agregar los import con los modelos implementados, esto crea la tabla en la base de datos.


app = FastAPI(
    title="Switcher - TuringSoft™",
    description="Descripcion de prueba.",
    version="0.1.0",
)

origins = ["http://localhost:5173",
           "http://localhost:5174",
           "http://localhost:5175"]

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

move_queries.test_create_move()