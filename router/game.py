from fastapi import APIRouter,HTTPException
from querys.game_queries import *
from querys.user_queries import *
from querys import remove_board,get_board,remove_all_moves
from schemas.response_models import InGame,BoardStatus
from utils.ws import manager
from utils.database import SERVER_DB

game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
async def leave(e: InGame):
    """Abandonar Partida."""
    # En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    if is_user_current_turn(e.id_game, e.id_player, SERVER_DB):
        remove_player(e.id_game,SERVER_DB)
        remove_user(e.id_player,SERVER_DB)
        reorder_turns(e.id_game,SERVER_DB)
        game_turn = (get_game_turn(e.id_game,SERVER_DB) % (get_players(e.id_game,SERVER_DB)))
        user_id = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
        await manager.broadcast(f"TURN {user_id}", e.id_game)
        await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)
    
    else:
        remove_player(e.id_game,SERVER_DB)
        remove_user(e.id_player,SERVER_DB)
        reorder_turns(e.id_game,SERVER_DB)
        await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)

    

    #Ganar por abando.
    if get_players(e.id_game,SERVER_DB) == 1 and get_game_state(e.id_game,SERVER_DB) == "Playing":
        set_game_state(e.id_game, "Finished",SERVER_DB)
        winner = get_users(e.id_game,SERVER_DB).users_list
        await manager.broadcast(f"{winner[0].id} WIN", e.id_game)

    #Cuando no queda ningun jugador se elimina partida.
    if get_players(e.id_game,SERVER_DB) == 0:
        remove_board(e.id_game,SERVER_DB)
        remove_all_moves(e.id_game,SERVER_DB)
        remove_game(e.id_game,SERVER_DB)

    
    return {"message": "Exit Successful."}


@game.post("/skip_turn")
async def skip(e: InGame):
    """Pasar el turno."""
    # En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.
    actual_turn = get_game_turn(e.id_game,SERVER_DB)
    actual_players = get_players(e.id_game,SERVER_DB)
    set_game_turn(e.id_game, (actual_turn + 1),SERVER_DB)
    game_turn = (get_game_turn(e.id_game,SERVER_DB) % actual_players)
    user_id = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
    await manager.broadcast(f"TURN {user_id}", e.id_game)

    return {"Skip Successful."}


@game.get("/game_status")
def get_status(id_player: int, id_game: int):
    """Consultar estado de partida/turnos."""

    # TODO Implementacion ->

    return {"Game Status Sucessful."}


@game.get("/board_status/{id_game}", response_model=BoardStatus)
def get_board_status(id_game: int):
    """Consultar estado del tablero."""
    if get_game(id_game=id_game,db=SERVER_DB) is not None:
        return BoardStatus(board=get_board(id_game=id_game, db=SERVER_DB))
    else:
        raise HTTPException(status_code=404, detail=f"El juego con id_game={id_game} no existe.")