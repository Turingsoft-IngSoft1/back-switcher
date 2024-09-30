from fastapi import APIRouter,HTTPException,WebSocket,WebSocketDisconnect

from querys.move_queries import set_users
from schemas.game_schema import Game
from schemas.user_schema import User
from schemas import response_models
from querys.user_queries import *
from querys.game_queries import *
from utils.ws import manager
from querys import game_queries
from schemas.response_models import InGame
game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
async def leave(e: InGame) :
    """Abandonar Partida."""
    #En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    remove_player(e.id_game)

    await manager.broadcast(f"{e.id_player} se fue", e.id_game)

    if get_players(e.id_game) == 1:
        set_game_state(e.id_game, "Finished")
        winner = get_users(e.id_game).users_list
        await manager.broadcast(f"{winner[0].id} gano", e.id_game)

    if get_players(e.id_game) == 0:
        remove_game(e.id_game)

    remove_user(e.id_player)

    return {"Exit Successful."}


@game.post("/skip_turn")
async def skip(e: InGame) :
    """Pasar el turno."""

    #En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.
    game_actual = game_queries.get_game(e.id_game)
    actual_turn = game_actual.turn
    game_queries.set_game_turn(e.id_game, ((actual_turn + 1) % game_actual.players)+1)
    
    await manager.broadcast(f"Turno {game_queries.get_game(e.id_game).turn}", e.id_game)
    
    return {"Skip Successful."}

@game.get("/game_status")
def get_status(id_player: int, id_game: int) :
    """Consultar estado de partida/turnos."""

    # TODO Implementacion ->
    
    return {"Game Status Sucessful."}


@game.get("/board_status")
def get_board(id_player: int, id_game: int) :
    """Consultar estado del tablero."""

    # TODO Implementacion ->

    return {"Board Status."}