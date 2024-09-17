from typing import Dict
from fastapi import APIRouter,HTTPException
from schemas.game_schema import Game
from schemas.user_schema import User
pre_game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/")
def user_data(id_user: int) :
    """Devolver data del usuario."""
    #Debe de alguna forma devolver los datos del usuario.
    #Para que el front lo pueda manejar.

    # TODO Implementacion ->
    usuario = User(id=2,name="Pepito")
    return usuario #Previsorio

@pre_game.post("/create_game")
def create(name: str, owner_name: str) :
    """Crear el juego."""
    #En caso de exito se debe retornar {id_player,id_game}.
    #Se debe crear un game_schema.Game.

    # TODO Implementacion ->
    
    return {"id_player": int,"id_game": int}

@pre_game.post("/join_game/{id_game}")
def join(id_game: int) -> int :
    """Unirse al juego."""

    #En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    #Se deben aplicar todos los cambios a la estructura interna de la paritda.

    # TODO Implementacion ->

    return  {"new_id": int}

@pre_game.get("/list_games")
def list_games() :
    """Listar los juegos creados."""

    #En caso de exito debe retornar un json con todos los juegos disponibles.
    example1 = Game(id=1,name="LaPartida1")
    example2 = Game(id=2,name="LaPartida2")
    dict_game: Dict[Game] = {1: example1, 2: example2,}

    # TODO Implementacion ->
    return dict_game

@pre_game.post("/start_game")
def start(id_game: int) :
    """Empezar un juego."""

    #En caso de exito debe iniciar la partida posteriormente sera implementado.
    #Actualizar los datos de la partida para que no se siga listando como disponible para unirse.

    # TODO Implementacion ->

    return {"El juego comenzo correctamente."}
