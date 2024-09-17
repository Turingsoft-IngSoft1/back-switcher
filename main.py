from fastapi import FastAPI
from router import pre_game,game

app = FastAPI(
    title="Switcher - TuringSoft™",
    description="Descripcion de prueba.",
    version="0.1.0",
)

app.include_router(pre_game,game)