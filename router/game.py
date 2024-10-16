from typing import  Dict
from fastapi import APIRouter,HTTPException
from querys.game_queries import *
from querys.user_queries import *
from querys import get_board,get_revealed_figures
from schemas.response_models import InGame,BoardStatus,UserData
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS
from utils.boardDetect import detect_figures
game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
async def leave(e: InGame):
    """Abandonar Partida."""
    # En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    if is_user_current_turn(e.id_game, e.id_player, SERVER_DB):
        set_game_turn(e.id_game, (get_game_turn(e.id_game,SERVER_DB) + 1),SERVER_DB)
        game_turn = (get_game_turn(e.id_game,SERVER_DB) % (get_players(e.id_game,SERVER_DB)))
        id_user = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
        await manager.broadcast(f"TURN {id_user}", e.id_game)

        remove_player(e.id_game,SERVER_DB)
        remove_user(e.id_player,SERVER_DB)
        reorder_turns(e.id_game,SERVER_DB)
        await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)
    
    else:
        remove_player(e.id_game,SERVER_DB)
        remove_user(e.id_player,SERVER_DB)
        reorder_turns(e.id_game,SERVER_DB)
        await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)

    #Ganar por abando.
    if get_players(e.id_game,SERVER_DB) == 1 and get_game_state(e.id_game,SERVER_DB) == "Playing":
        set_game_state(e.id_game, "Finished",SERVER_DB)
        winner = get_users(e.id_game,SERVER_DB)
        await manager.broadcast(f"{winner[0].id} WIN", e.id_game)

    #Cuando no queda ningun jugador se elimina partida.
    if get_players(e.id_game,SERVER_DB) == 0:
        remove_game(e.id_game,SERVER_DB)
        PARTIAL_BOARDS.remove(e.id_game)

    return {"message": "Exit Successful."}


@game.post("/skip_turn")
async def skip(e: InGame):
    """Pasar el turno."""
    # En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.
    actual_turn = get_game_turn(e.id_game,SERVER_DB)
    actual_players = get_players(e.id_game,SERVER_DB)
    set_game_turn(e.id_game, (actual_turn + 1),SERVER_DB)
    game_turn = (get_game_turn(e.id_game,SERVER_DB) % actual_players)
    id_user = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
    await manager.broadcast(f"TURN {id_user}", e.id_game)

    return {"Skip Successful."}


@game.get("/game_status/{id_game}",response_model=list[UserData])
async def get_status(id_game: int):
    """Consultar estado de partida/turnos."""
    rf = get_revealed_figures(id_game,SERVER_DB)
    users = get_users(id_game,SERVER_DB)
    response = []
    for u in users:
        response.append(UserData(id_user=u.id,name=u.name,figures=rf[u.id]))
    return response


@game.get("/board_status/{id_game}", response_model=BoardStatus)
async def get_board_status(id_game: int):
    """Consultar estado del tablero."""
    if get_game(id_game=id_game,db=SERVER_DB) is not None:
        return BoardStatus(board=get_board(id_game=id_game, db=SERVER_DB))
    else:
        raise HTTPException(status_code=404, detail=f"El juego con id_game={id_game} no existe.")

@game.get("/detect_figures_on_board/{id_game}/{id_user}")
async def detect_figures_on_board(id_game: int, id_user: int):
    if (g := get_game(id_game=id_game, db=SERVER_DB)) is not None and (g.state == "Playing"):
        rf = get_revealed_figures(id_game,SERVER_DB)
        figures = set(rf[id_user])
        detected_figures = detect_figures(PARTIAL_BOARDS.get(id_game),figures)
        response: Dict[str, Dict[str, list]] = {}
        for detected_fig in detected_figures:
            if detected_fig[1] not in response:
                response[detected_fig[1]] = {}
            if detected_fig[0] not in response[detected_fig[1]]:
                response[detected_fig[1]][detected_fig[0]] = []
            response[detected_fig[1]][detected_fig[0]].append(detected_fig[2])
        return response
    else:
        raise HTTPException(status_code=404, detail=f"El juego con id_game={id_game} no existe o todavia no comenzo.")