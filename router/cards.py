from fastapi import APIRouter

from querys.game_queries import *
from querys.user_queries import *
from querys.move_queries import *
from querys.figure_queries import *
from schemas.response_models import *
from utils.ws import manager
from utils.database import SERVER_DB

cards = APIRouter()


@cards.get("/get_moves")
async def get_moves(player_id: int, game_id: int):
    """Obtener cartas de movimiento."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.
    moves = [[],[],[],[],[],[],[]]

    i=0
    while i<3:   
        random_move = random.sample(moves, 1)[0]
        if get_move_pile(random_move, SERVER_DB)=="Deck":
            set_move_pile(random_move, "In Hand", SERVER_DB)
            set_users(random_move, player_id, SERVER_DB)
            remove_move_from_deck(game_id, SERVER_DB)
            await manager.send_personal_message(random_move, game_id, player_id)
            i+=1

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
