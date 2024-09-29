from fastapi import APIRouter,HTTPException,WebSocket,WebSocketDisconnect
from schemas.game_schema import Game
from schemas.user_schema import User
from schemas.response_models import *
from querys.user_queries import *
from querys.game_queries import *
from utils.ws import manager

pre_game = APIRouter()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/user/{id_user}",response_model=int)
def user_data(id_user: int) :
    """Devolver data del usuario."""
    #Debe de alguna forma devolver los datos del usuario.
    #Para que el front lo pueda manejar.
    # TODO Arreglar ->
    g = get_game(id_user)

    return g.id

@pre_game.get("/active_players/{id_game}",response_model=CurrentUsers)
def get_active_players(id_game: int) :
    """Devuelve los jugadors conectados a una partida."""
    return get_users(id_game)

@pre_game.post("/create_game",response_model=ResponseCreate)
def create(e: CreateEntry) :
    """Crear el juego."""
    #En caso de exito se debe retornar {id_player,id_game}.
    #Se debe crear un game_schema.Game.
    # TODO Agregar TESTs ->

    new_game_id = create_game(name=e.game_name, max_players=e.max_player, min_players=e.min_player)
    new_user_id = create_user(name=e.owner_name,game_id=new_game_id)
    set_game_host(id_game=new_game_id,host=new_user_id)

    return ResponseCreate(id_game=new_game_id,id_player=new_user_id)

@pre_game.post("/join_game",response_model=ResponseJoin)
def join(e: JoinEntry) :
    """Unirse al juego."""

    #En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    #Se deben aplicar todos los cambios a la estructura interna de la paritda.
    # TODO Testing ->
    if get_max_players(e.id_game) > get_players(e.id_game):
        add_player(e.id_game)
        p_id = create_user(name=e.player_name,game_id=e.id_game)
    else:
        raise HTTPException(status_code=409, detail="El lobby está lleno.")

    return ResponseJoin(new_player_id=p_id)

@pre_game.get("/list_games",response_model=ResponseList)
def list_games() :
    """Listar los juegos creados."""

    #En caso de exito debe retornar un json con todos los juegos disponibles.
    # TODO Testing ->
    g_list = listing_games()

    return ResponseList(games_list=g_list)

@pre_game.post("/start_game/{game_id}")
async def start(game_id: int) :
    """Empezar un juego."""

    #En caso de exito debe iniciar la partida posteriormente sera implementado.
    #Actualizar los datos de la partida para que no se siga listando como disponible para unirse.
    #Tiene que repartir las cartas a todos los jugadores.
    #Tiene que cambiar el estado a "Playing".
    #Tiene que inicializar el tablero randomizado.
    #Tiene que avisar a todos los clientes.

    if get_players(game_id) >= get_min_players(game_id):
        set_game_state(game_id, "Playing")

        await manager.broadcast(f"GAME_STARTED", game_id)

    else:
        raise HTTPException(status_code=409, detail="El lobby no alcanzo su capacidad minima para comenzar.")

    return {"message": "El juego comenzo correctamente."}

@pre_game.websocket("/ws/{game_id}/{user_id}")
async def websocket_endpoint(ws: WebSocket, game_id: int, user_id: int) :
    await manager.connect(ws, game_id, user_id)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws, game_id, user_id)
