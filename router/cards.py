from fastapi import APIRouter
from querys.move_queries import *
from querys.game_queries import *
from schemas.response_models import *
from utils.ws import manager
from utils.database import SERVER_DB

import random

cards = APIRouter()

@cards.post("/get_moves/{id_game}/{id_player}", response_model=ResponseMoves)
def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.
    
    in_hand = moves_in_hand(id_game, id_player, SERVER_DB)
    if moves_in_deck(id_game, SERVER_DB) < (3-in_hand):
        refill_moves(id_game, SERVER_DB)
    
    deck = random.sample(get_deck(id_game, SERVER_DB), 3-in_hand)
    
    moves = []
    for i in deck:
        set_move_user(i, id_player, SERVER_DB)
        set_move_status(i, "InHand", SERVER_DB)
        moves.append(get_move_name(i, SERVER_DB))
    
    return ResponseMoves(moves=moves)


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
