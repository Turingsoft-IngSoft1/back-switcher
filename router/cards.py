from fastapi import APIRouter,HTTPException
from schemas import game_schema

cards = APIRouter()

@cards.get("/get_moves/{id_player}")
def get_moves(id_player: int) :
    """Obtener cartas de movimiento."""

    #En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # Implementacion ->

    return {"Movimientos Entregados Correctamente."}

@cards.post("/use_moves/{id_player}")
def use_moves(id_player: int) :
    """Usar una carta de movimiento."""

    # Implementacion ->

    return {"Movimientos Usados Correctamente."}

@cards.get("/get_shape/{id_player}")
def get_shape(id_player: int) :
    """Obtener cartas de figura."""

    #En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # Implementacion ->

    return {"Figuras Entregadas Correctamente."}

@cards.post("/use_shape/{id_player}")
def use_shape(id_player: int) :
    """Usar una carta de figura."""

    # Implementacion ->

    return {"Figuras Usadas Correctamente."}