from fastapi import APIRouter,HTTPException
from schemas.user_schema import User
from querys import game_queries,user_queries
from schemas.response_models import *

pre_game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/user/{id_user}")
def user_data(id_user: int) :
    """Devolver data del usuario."""
    #Debe de alguna forma devolver los datos del usuario.
    #Para que el front lo pueda manejar.
    u = user_queries.get_games(id_user)
    # TODO Implementacion ->
    usuario = User(id=u.id,name=u.name,game=u.game)
    return usuario #Previsorio

@pre_game.post("/create_game",response_model=ResponseCreate)
def create(e: CreateEntry) :
    """Crear el juego."""
    new_game_id = game_queries.create_game(e.game_name,e.owner_name,e.min_player,e.max_player)
    new_user_id = user_queries.create_user(e.owner_name,new_game_id)
    return ResponseCreate(id_game=new_game_id,id_player=new_user_id)

@pre_game.post("/join_game",response_model=ResponseJoin)
def join(id_game: int) :
    """Unirse al juego."""

    #En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    #Se deben aplicar todos los cambios a la estructura interna de la paritda.

    # TODO Implementacion ->

    return ResponseJoin(new_id_player=1)

@pre_game.get("/list_games",response_model=ResponseList)
def list_games() :
    """Listar los juegos creados."""

    #En caso de exito debe retornar un json con todos los juegos disponibles.
    games_listed = game_queries.list_games()
    # TODO Implementacion ->
    return ResponseList(games_list=games_listed)

@pre_game.post("/start_game")
def start(id_game: int) :
    """Empezar un juego."""

    #En caso de exito debe iniciar la partida posteriormente sera implementado.
    #Actualizar los datos de la partida para que no se siga listando como disponible para unirse.

    # TODO Implementacion ->

    return {"El juego comenzo correctamente."}
