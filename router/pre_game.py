from fastapi import APIRouter,HTTPException
from schemas.game_schema import Game
from schemas.user_schema import User
from typing import Dict

pre_game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/")
def user_data(id_user: int) :
    """Devolver data del usuario."""
    #Debe de alguna forma devolver los datos del usuario.
    #Para que el front lo pueda manejar.

    # Implementacion ->

    return {"user": User} #Previsorio

@pre_game.post("/create_game")
def create() -> dict[int, int] :
    """Crear el juego."""
    #En caso de exito se debe retornar {id_player,id_game}.
    #Se debe crear un game_schema.Game.

    # Implementacion ->
    
    return {"id_player": int,"id_game": int}

@pre_game.post("/join_game/{id_game}")
def join(id_game: int) :
    """Unirse al juego."""

    #En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    #Se deben aplicar todos los cambios a la estructura interna de la paritda.

    # Implementacion ->

    return  {"Connection Successful."}

@pre_game.get("/list_game")
def list_game() :
    """Listar los juegos creados."""

    #En caso de exito debe retornar un json con todos los juegos disponibles.
    example1 = Game(id=1,name="LaPartida1")
    example2 = Game(id=2,name="LaPartida2")
    # Implementacion ->
    dict_game: Dict[Game] = {1: example1, 2: example2,}
    return dict_game
    #Completar luegon de la implementacion definitiva

@pre_game.get("/list_game/{id_game}")
def game_data(id_game: int) :
    """Devolver data de un juego especifico."""

    #En caso que el id exista retorna la informacion de la partido.

    # Implementacion ->

    return {"game": Game} #Previsorio


@pre_game.post("/start_game/{id_game}")
def start(id_game: int) :
    """Empezar un juego."""

    #En caso de exito debe iniciar la partida posteriormente sera implementado.
    #Actualizar los datos de la partida para que no se siga listando como disponible para unirse.

    # Implementacion ->

    return {"El juego comenzo correctamente."}
