from fastapi import APIRouter,HTTPException

from schemas.game_schema import Game
from schemas.user_schema import User
from schemas.response_models import ResponseCreate,ResponseJoin,ResponseList,CreateEntry
from querys.user_queries import get_games, create_user
from querys.game_queries import *
pre_game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/user/{id_user}")
def user_data(id_user: int) :
    """Devolver data del usuario."""
    #Debe de alguna forma devolver los datos del usuario.
    #Para que el front lo pueda manejar.
    # TODO Cambiar ->

    current_game = get_game(id_user)

    return current_game

@pre_game.post("/create_game",response_model=ResponseCreate)
def create(e: CreateEntry) :
    """Crear el juego."""
    #En caso de exito se debe retornar {id_player,id_game}.
    #Se debe crear un game_schema.Game.
    # TODO Agregar TESTs ->

    new_game_id = create_game(name=e.game_name, max_players=e.max_player, min_players=e.min_player)
    new_user_id = create_user(name=e.owner_name,game_id=new_game_id)
    set_game_host(id_game=new_game_id,host=new_user_id)

    return ResponseCreate(game_id=new_game_id,user_id=new_user_id)

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
    example1 = Game(id=1,name="LaPartida1",isFull=False)
    example2 = Game(id=2,name="LaPartida2",isFull=True)

    # TODO Implementacion ->
    return ResponseList(games_list=[example1,example2])

@pre_game.post("/start_game")
def start(id_game: int) :
    """Empezar un juego."""

    #En caso de exito debe iniciar la partida posteriormente sera implementado.
    #Actualizar los datos de la partida para que no se siga listando como disponible para unirse.

    # TODO Implementacion ->

    return {"El juego comenzo correctamente."}
