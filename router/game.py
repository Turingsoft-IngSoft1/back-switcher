from fastapi import APIRouter,HTTPException
from schemas import game_schema

game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game/{id_player}")
def leave(id_player: int, id_game: int) :
    """Abandonar Partida."""
    #En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    #Debe avisar al resto de jugadores por WebSockets ?

    # Implementacion ->

    return {"id_player": int}

@game.post("/skip_turn/{id_player}")
def skip(id_player: int, id_game: int) :
    """Pasar el turno."""

    #En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.

    # Implementacion ->

    return {"id_player": int}

@game.post("/game_status/{id_player}")
def get_status(id_player: int, id_game: int) :
    """Consultar estado de partida/turnos."""

    # Implementacion ->

    return {"id_player": int}


@game.post("/board_status/{id_player}")
def get_board(id_player: int, id_game: int) :
    """Consultar estado del tablero."""

    # Implementacion ->

    return {"id_player": int}