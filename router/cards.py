from fastapi import APIRouter, HTTPException
from querys.move_queries import *
from querys.game_queries import *
from querys.user_queries import *
from schemas.response_models import *
from utils.ws import manager
from utils.database import SERVER_DB

import random

cards = APIRouter()

@cards.post("/get_moves/{id_game}/{id_player}", response_model=ResponseMoves)
def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.
    
    if game_exists(id_game, SERVER_DB):
        if user_exists(id_player, SERVER_DB):
            if get_game_state(id_game, SERVER_DB) == "Playing":
                in_hand = moves_in_hand(id_game, id_player, SERVER_DB)
                if moves_in_deck(id_game, SERVER_DB) < (3-in_hand):
                    refill_moves(id_game, SERVER_DB)
    
                deck = random.sample(get_deck(id_game, SERVER_DB), 3-in_hand)
    
                for i in deck:
                    set_move_user(i, id_player, SERVER_DB)
                    set_move_status(i, "InHand", SERVER_DB)
    
                hand = get_hand(id_game, id_player, SERVER_DB)
            
            else:
                raise HTTPException(status_code=409, detail="La partida no ha iniciado aun.")
        
        else:
            raise HTTPException(status_code=404, detail="El jugador con el ID ingresado no existe.")
        
    else:
        raise HTTPException(status_code=404, detail="La partida con el ID ingresado no existe.")
        
    return ResponseMoves(moves=hand)


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
