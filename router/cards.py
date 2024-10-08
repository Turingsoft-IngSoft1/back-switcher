from fastapi import APIRouter
from querys.move_queries import *
from utils.ws import manager
from utils.database import SERVER_DB

import random

cards = APIRouter()


@cards.get("/get_moves")
def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.
    
    in_hand = moves_in_hand(id_game, id_player, SERVER_DB)
    if moves_in_deck(id_game, SERVER_DB) < (3-in_hand):
        refill_moves(id_game, SERVER_DB)
    
    deck = get_deck(id_game, SERVER_DB)
    deck = random.sample()
    
    for _ in range(3-in_hand):
        set_move_user(deck.pop(), id_player, SERVER_DB)
    
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
