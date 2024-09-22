from fastapi import FastAPI
from router.pre_game import pre_game
from router.game import game
from router.cards import cards
from models.base import Base, engine
from models.game import GameTable
from tests.gameCreation import testGameCreation

# TODO -> Agregar los import con los modelos implementados, esto crea la tabla en la base de datos.

app = FastAPI(
    title="Switcher - TuringSoft™",
    description="Descripcion de prueba.",
    version="0.1.0",
)

app.include_router(pre_game)
app.include_router(game)
app.include_router(cards)

# Crea las tablas en base a los models importados.
Base.metadata.create_all(bind=engine)

testGameCreation()
