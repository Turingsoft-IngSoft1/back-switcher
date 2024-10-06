from fastapi import APIRouter
from querys.game_queries import *
from querys.user_queries import *
from querys import remove_board
from schemas.response_models import InGame
from utils.ws import manager
from utils.database import SERVER_DB

game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
async def leave(e: InGame):
    """Abandonar Partida."""
    # En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    remove_player(e.id_game,SERVER_DB)
    remove_user(e.id_player,SERVER_DB)
    await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)

    if get_players(e.id_game,SERVER_DB) == 1 and get_game_state(e.id_game,SERVER_DB) == "Playing":
        set_game_state(e.id_game, "Finished",SERVER_DB)
        winner = get_users(e.id_game,SERVER_DB).users_list
        await manager.broadcast(f"{winner[0].id} WIN", e.id_game)

    if get_players(e.id_game,SERVER_DB) == 0:
        remove_board(e.id_game,SERVER_DB)
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
    uid = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
    await manager.broadcast(f"TURN {uid}", e.id_game)

    return {"Skip Successful."}


@game.get("/game_status")
def get_status(id_player: int, id_game: int):
    """Consultar estado de partida/turnos."""

    # TODO Implementacion ->

    return {"Game Status Sucessful."}


@game.get("/board_status")
def get_board(id_player: int, id_game: int):
    """Consultar estado del tablero."""

    # TODO Implementacion ->

    return {"Board Status."}
