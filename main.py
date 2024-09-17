from fastapi import FastAPI,APIRouter
from router.pre_game import pre_game
from router.game import game
from router.cards import cards

app = FastAPI(
    title="Switcher - TuringSoft™",
    description="Descripcion de prueba.",
    version="0.1.0",
)

app.include_router(pre_game)
app.include_router(game)
app.include_router(cards)
