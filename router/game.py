from fastapi import APIRouter
from querys.game_queries import *
from querys.user_queries import *
from schemas.response_models import InGame
from utils.ws import manager

game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
async def leave(e: InGame):
    """Abandonar Partida."""
    # En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    remove_player(e.id_game)
    remove_user(e.id_player)
    await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)

    if get_players(e.id_game) == 1 and get_game_state(e.id_game) == "Playing":
        set_game_state(e.id_game, "Finished")
        winner = get_users(e.id_game).users_list
        await manager.broadcast(f"{winner[0].id} WIN", e.id_game)

    if get_players(e.id_game) == 0:
        remove_game(e.id_game)

    return {"message": "Exit Successful."}


@game.post("/skip_turn")
async def skip(e: InGame):
    """Pasar el turno."""

    # En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.
    actual_turn = get_game_turn(e.id_game)
    actual_players = get_players(e.id_game)
    set_game_turn(e.id_game, (actual_turn + 1))
    game_turn = (get_game_turn(e.id_game) % actual_players)
    await manager.broadcast(f"TURN {game_turn}", e.id_game)

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
