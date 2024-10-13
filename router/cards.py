from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from querys.move_queries import *
from querys.game_queries import *
from querys.figure_queries import *
from querys.board_queries import *

from schemas.response_models import *
from schemas.move_schema import Move
from utils.ws import manager
from utils.database import SERVER_DB

import random

cards = APIRouter()

@cards.post("/get_moves/{id_game}/{id_player}", response_model=ResponseMoves)
async def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""

    in_hand = moves_in_hand(id_game, id_player, SERVER_DB)
    if moves_in_deck(id_game, SERVER_DB) < (3-in_hand):
        refill_moves(id_game, SERVER_DB)
    if in_hand < 3:
        current_hand = refill_hand(id_game,id_player,in_hand,SERVER_DB)    
    else:
        current_hand = get_hand(id_game,id_player,SERVER_DB)
    return ResponseMoves(moves=current_hand)


@cards.post("/use_moves")
async def use_moves(e: EntryMove):
    """Usar una carta de movimiento."""
    move = Move(name=e.name, initial_position=e.pos1)
    if (e.name not in get_hand(e.id_game, e.id_player, SERVER_DB)):
        raise HTTPException(status_code=400, detail="El usuario no tiene ese movimiento.")
    if (e.pos2 not in move.available_moves):
        raise HTTPException(status_code=400, detail="Movimiento invalido.")
    use_move(e.id_game, e.id_player, e.name, SERVER_DB)
    try:
        board = get_board(e.id_game, SERVER_DB)
        board[e.pos1[1]][e.pos1[0]], board[e.pos2[1]][e.pos2[0]] = (
            board[e.pos2[1]][e.pos2[0]],
            board[e.pos1[1]][e.pos1[0]],
        )
        update_board(e.id_game, board, SERVER_DB)
    except BoardValidationError:
        return JSONResponse(status_code=400, content={"detail": "Error al actualizar el tablero."})
        
    await manager.broadcast("REFRESH_BOARD",e.id_game)
    return {"Movimiento Realizado Correctamente."}

@cards.get("/get_figure/{id_game}/{id_player}")
async def get_figure(id_player: int, id_game: int):
    """Obtener cartas de figura."""

    in_hand = figures_in_hand(id_game, id_player, SERVER_DB)
    if in_hand < 3:
        refill_revealed_figures(id_game,id_player, SERVER_DB)
        manager.broadcast("REFRESH_FIGURES",id_game)
    else:
        raise HTTPException(status_code=400, detail="No se pueden obtener mas figuras.")

@cards.post("/use_figure")
def use_figure(id_player: int, id_game: int):
    """Usar una carta de figura."""

    # TODO Implementacion ->

    return {"Figuras Usadas Correctamente."}
