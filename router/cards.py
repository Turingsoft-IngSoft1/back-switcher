from fastapi import APIRouter, HTTPException
from querys.move_queries import *
from querys.game_queries import *
from schemas.response_models import *
from querys import get_revealed_figures, refill_revealed_figures, figures_in_hand, get_user_from_turn
from utils.ws import manager
from utils.database import SERVER_DB

cards = APIRouter()

@cards.post("/get_moves/{id_game}/{id_player}", response_model=ResponseMoves)
async def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""

    in_hand = moves_in_hand(id_game, id_player, SERVER_DB)
    if moves_in_deck(id_game, SERVER_DB) < (3-in_hand):
        refill_moves(id_game, SERVER_DB)
    if in_hand < 3:
        current_hand = refill_hand(id_game, id_player, in_hand, SERVER_DB)    
    else:
        current_hand = get_hand(id_game, id_player, SERVER_DB)
        
    return ResponseMoves(moves=current_hand)


@cards.post("/use_moves")
def use_moves(id_player: int, id_game: int):
    """Usar una carta de movimiento."""

    # TODO Implementacion ->

    return {"Movimientos Usados Correctamente."}


@cards.get("/get_figures/{id_game}/{id_player}")
async def get_figures(id_player: int, id_game: int):
    """Obtener cartas de figura."""

    in_hand = figures_in_hand(id_game, id_player, SERVER_DB)
    if in_hand < 3:
        refill_revealed_figures(id_game, id_player, SERVER_DB)
        await manager.broadcast("REFRESH_FIGURES", id_game)
    
    return get_revealed_figures(id_game, SERVER_DB)[id_player]

@cards.post("/use_figures")
def use_figures(id_player: int, id_game: int):
    """Usar una carta de figura."""

    # TODO Implementacion ->

    return {"Figuras Usadas Correctamente."}
