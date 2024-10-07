from fastapi import APIRouter

from querys.game_queries import *
from querys.user_queries import *
from querys.move_queries import *
from querys.figure_queries import *
from schemas.response_models import *
from utils.ws import manager

cards = APIRouter()


@cards.get("/get_moves")
async def get_moves(player_id: int, game_id: int):
    """Obtener cartas de movimiento."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.


    return {"Movimientos Entregados Correctamente."}


@cards.post("/use_moves")
def use_moves(id_player: int, id_game: int):
    """Usar una carta de movimiento."""

    # TODO Implementacion ->

    return {"Movimientos Usados Correctamente."}


@cards.get("/get_figure")
def get_figure(id_player: int, id_game: int):
    """Obtener cartas de figura."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # TODO Implementacion ->

    return {"Figuras Entregadas Correctamente."}


@cards.post("/use_figure")
def use_figure(id_player: int, id_game: int):
    """Usar una carta de figura."""

    # TODO Implementacion ->

    return {"Figuras Usadas Correctamente."}
