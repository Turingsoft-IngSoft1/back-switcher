from fastapi import APIRouter, HTTPException

from querys.move_queries import *
from querys.game_queries import *
from querys.figure_queries import *
from querys.board_queries import *
from querys import is_user_current_turn

from schemas.response_models import *
from schemas.move_schema import Move
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS

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
    if  not is_user_current_turn(e.id_game, e.id_player, SERVER_DB):
        raise HTTPException(status_code=412, detail="El jugador no se encuentra en su turno.")
    
    if (e.name not in get_hand(e.id_game, e.id_player, SERVER_DB)):
        raise HTTPException(status_code=404, detail="El usuario no tiene ese movimiento.")
    
    move = Move(name=e.name, initial_position=e.pos1)
    if (e.pos2 not in move.available_moves):
        raise HTTPException(status_code=409, detail="Movimiento invalido.")
    
    use_move(e.id_game, e.id_player, e.name, SERVER_DB)
    PARTIAL_BOARDS.update(e.id_game,e.pos1,e.pos2)
    update_board(id_game=e.id_game,
                 matrix=PARTIAL_BOARDS.get(e.id_game),
                 db=SERVER_DB)
    await manager.broadcast(f"MOVE {e.pos1} {e.pos2}",e.id_game)
    return {"Movimiento Realizado Correctamente."}

@cards.post("/get_figure/{id_game}/{id_player}")
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
