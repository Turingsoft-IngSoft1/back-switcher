from fastapi import APIRouter,HTTPException
from schemas import game_schema
from utils.ws import manager
from querys import game_queries
from schemas.response_models import InGame
game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
def leave(id_player: int, id_game: int) :
    """Abandonar Partida."""
    #En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    #Debe avisar al resto de jugadores por WebSockets ?

    # TODO Implementacion ->

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