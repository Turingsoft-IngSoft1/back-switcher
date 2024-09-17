from fastapi import APIRouter,HTTPException
from schemas import game_schema

cards = APIRouter()

@cards.get("/get_moves")
def get_moves(id_player: int, id_game: int) :
    """Obtener cartas de movimiento."""

    #En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # TODO Implementacion ->

    return {"Movimientos Entregados Correctamente."}

@cards.post("/use_moves")
def use_moves(id_player: int, id_game: int) :
    """Usar una carta de movimiento."""

    # TODO Implementacion ->

    return {"Movimientos Usados Correctamente."}

@cards.get("/get_shape")
def get_shape(id_player: int, id_game: int) :
    """Obtener cartas de figura."""

    #En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # TODO Implementacion ->

    return {"Figuras Entregadas Correctamente."}

@cards.post("/use_shape")
def use_shape(id_player: int, id_game: int) :
    """Usar una carta de figura."""

    # TODO Implementacion ->

    return {"Figuras Usadas Correctamente."}