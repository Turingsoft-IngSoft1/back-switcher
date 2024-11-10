from fastapi import APIRouter, HTTPException

from querys.move_queries import *
from querys.game_queries import *
from querys.figure_queries import *
from querys.board_queries import *
from querys import is_user_current_turn
from querys import figure_queries

from schemas.response_models import *
from schemas.move_schema import Move
from schemas.figure_schema import Figure
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS
from utils.boardDetect import detect_figures
from querys import get_game

cards = APIRouter()

@cards.post("/get_moves/{id_game}/{id_player}", response_model=ResponseMoves)
async def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""
    if get_game(id_game=id_game,db=SERVER_DB) is None:
        raise HTTPException(status_code=404, detail=f"El juego con id_game={id_game} no existe.")
   
    in_hand = moves_in_hand(id_game, id_player, SERVER_DB)
    if moves_in_deck(id_game, SERVER_DB) < (3-in_hand):
        refill_moves(id_game, SERVER_DB)
    if in_hand < 3:
        refill_hand(id_game, id_player, (3-in_hand), SERVER_DB)
    
    current_hand = get_hand(id_game, id_player, SERVER_DB)

    return ResponseMoves(moves=current_hand)


@cards.post("/use_moves")
async def use_moves(e: EntryMove):
    """Usar una carta de movimiento."""
    
    if  not is_user_current_turn(e.id_game, e.id_player, SERVER_DB):
        raise HTTPException(status_code=412, detail="El jugador no se encuentra en su turno.")

    if e.name not in get_hand(e.id_game, e.id_player, SERVER_DB):
        raise HTTPException(status_code=404, detail="El usuario no tiene ese movimiento.")

    move = Move(name=e.name, initial_position=e.pos1)
    if e.pos2 not in move.available_moves:
        raise HTTPException(status_code=409, detail="Movimiento invalido.")

    use_move(e.id_game, e.id_player, e.name, SERVER_DB)
    PARTIAL_BOARDS.update(e.id_game,e.pos1,e.pos2)
    await manager.broadcast(f"MOVE {e.pos1} {e.pos2}",e.id_game)
    return {"Movimiento Realizado Correctamente."}

@cards.post("/get_figures/{id_game}/{id_player}")
async def get_figures(id_player: int, id_game: int):
    """Obtener cartas de figura."""
    in_hand = figures_in_hand(id_game, id_player, SERVER_DB)
    if in_hand < 3 and (not is_user_blocked(id_game, id_player, SERVER_DB)):
        refill_revealed_figures(id_game,id_player, SERVER_DB)
        await manager.broadcast("REFRESH_FIGURES",id_game)
        return {"Se entregaron las figuras correctamente."}
    else:
        return {"El jugador no puede obtener mas cartas."}

@cards.post("/use_figures")
async def use_figures(e: EntryFigure):
    """Usar una carta de figura."""
    if  not is_user_current_turn(e.id_game, e.id_player, SERVER_DB):
        raise HTTPException(status_code=412, detail="El jugador no se encuentra en su turno.")

    if not e.name in get_revealed_figures(e.id_game, SERVER_DB)[e.id_player]:
        raise HTTPException(status_code=404, detail="El usuario no tiene ese esa figura en su mano.")
    
    detected_figures = detect_figures(PARTIAL_BOARDS.get(e.id_game), [e.name])
    found = False
    color = "NOT"
    for color_detected , _ , group_detected in detected_figures:
        if set(e.figure_pos) == set(group_detected):
            found = True
            color = color_detected
            break
    
    if not found:
        raise HTTPException(status_code=404, detail="La figura no se encuentra en el tablero.")
    elif color == get_color(e.id_game, SERVER_DB):
        raise HTTPException(status_code=409, detail="El color de la figura está bloqueado.")

    if get_played(e.id_game, SERVER_DB) > 0:
        discard_move(e.id_game, e.id_player, SERVER_DB)
        
    use_figure(e.id_game, e.id_player, e.name, SERVER_DB)
    unblock_figure(e.id_game, e.id_player, SERVER_DB)
    update_board(id_game=e.id_game,
                 matrix=PARTIAL_BOARDS.get(e.id_game),
                 db=SERVER_DB)
    update_color(e.id_game, color, SERVER_DB)
    await manager.broadcast("REFRESH_BOARD", e.id_game)
    await manager.broadcast("REFRESH_FIGURES", e.id_game)

    in_deck = figures_in_deck(e.id_game, e.id_player, SERVER_DB)
    in_hand = figures_in_hand(e.id_game, e.id_player, SERVER_DB)
    if in_deck + in_hand == 0:
        set_game_state(e.id_game, "Finished", SERVER_DB)
        await manager.broadcast(f"{e.id_player} WIN", e.id_game)
    
    return {"Figuras Usadas Correctamente."}

@cards.post("/cancel_moves/{id_game}")
async def cancel_moves(id_game: int):
    """Cancelar movimientos parciales."""
    
    if get_played(id_game, SERVER_DB) > 0:
        unplay_moves(id_game, SERVER_DB)
        PARTIAL_BOARDS.remove(id_game)
        PARTIAL_BOARDS.initialize(id_game, SERVER_DB)
        await manager.broadcast("REFRESH_BOARD", id_game)
    
        return {"message": "Movimientos cancelados correctamente."}
    else:
        return {"message": "No hay movimientos para cancelar."}

@cards.post("/block_figure/")
async def block_figure_action(e: FigureBlock):
    """Bloquea una figura."""
    if  not is_user_current_turn(e.id_game, e.id_caller, SERVER_DB):
        raise HTTPException(status_code=412, detail="El jugador no se encuentra en su turno.")
    if not e.figure_name in get_revealed_figures(e.id_game, SERVER_DB)[e.id_target]:
        raise HTTPException(status_code=404, detail="Esa figura no se encuntra encuentra en la mano de ningun usuario.")
    
    detected_figures = detect_figures(PARTIAL_BOARDS.get(e.id_game), [e.figure_name])
    found = False
    color= 'NOT'
    for color_detected , _ , group_detected in detected_figures:
        if set(e.pos) == set(group_detected):
            found = True
            color = color_detected
            break
    
    if not found:
        raise HTTPException(status_code=404, detail="La figura no se encuentra en el tablero.")
    elif color == get_color(e.id_game, SERVER_DB):
        raise HTTPException(status_code=409, detail="El color de la figura está bloqueado.")
    
    if  is_user_blocked(e.id_game, e.id_target, SERVER_DB):
        raise HTTPException(status_code=409, detail="El jugador ya tiene una figura bloqueada.")
    
    if get_played(e.id_game, SERVER_DB) > 0:
        discard_move(e.id_game, e.id_caller, SERVER_DB)

    block_figure(e.id_game, e.id_target, e.figure_name, SERVER_DB)
    update_board(id_game=e.id_game,
                 matrix=PARTIAL_BOARDS.get(e.id_game),
                 db=SERVER_DB)
    update_color(e.id_game, color, SERVER_DB)
    await manager.broadcast("REFRESH_FIGURES", e.id_game)
    return {"message": "Figura bloqueada correctamente."}
