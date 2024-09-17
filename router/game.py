from fastapi import APIRouter,HTTPException
from schemas import game_schema

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
def skip(id_player: int, id_game: int) :
    """Pasar el turno."""

    #En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.

    # TODO Implementacion ->

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