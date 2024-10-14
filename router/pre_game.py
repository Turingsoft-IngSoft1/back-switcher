from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from querys.game_queries import *
from querys.user_queries import *
from querys.move_queries import *
from querys.figure_queries import *
from schemas.response_models import *
from querys import create_board
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS

pre_game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/")
def default():
    """Mensaje predeterminado."""
    return f"El Switcher."


@pre_game.get("/active_players/{id_game}", response_model=CurrentUsers)
def get_active_players(id_game: int):
    """Devuelve los jugadors conectados a una partida."""
    return get_users(id_game=id_game,
                     db=SERVER_DB)


@pre_game.post("/create_game", response_model=ResponseCreate)
def create(e: CreateEntry):
    """Crear el juego."""
    # En caso de exito se debe retornar {id_player,id_game}.
    # Se debe crear un game_schema.Game.
    # TODO Agregar TESTs ->

    new_id_game = create_game(name=e.game_name,
                              max_players=e.max_player,
                              min_players=e.min_player,
                              db=SERVER_DB)
    
    new_user_id = create_user(name=e.owner_name,
                              id_game=new_id_game,
                              db=SERVER_DB)
    
    set_game_host(id_game=new_id_game,
                  host=new_user_id,
                  db=SERVER_DB)
    
    create_board(id_game=new_id_game,
                 db=SERVER_DB)

    return ResponseCreate(id_game=new_id_game, id_player=new_user_id)


@pre_game.post("/join_game", response_model=ResponseJoin)
async def join(e: JoinEntry):
    """Unirse al juego."""

    # En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    # Se deben aplicar todos los cambios a la estructura interna de la paritda.
    # TODO Testing ->
    if get_max_players(e.id_game,SERVER_DB) > get_players(e.id_game,SERVER_DB):
        
        add_player(id_game=e.id_game,
                   db=SERVER_DB)
        p_id = create_user(name=e.player_name,
                           id_game=e.id_game,
                           db=SERVER_DB)
        await manager.broadcast(f"{p_id} JOIN",e.id_game)
        
    else:
        raise HTTPException(status_code=409, detail="El lobby está lleno.")

    return ResponseJoin(new_player_id=p_id)


@pre_game.get("/list_games", response_model=ResponseList)
async def list_games():
    """Listar los juegos creados."""

    # En caso de exito debe retornar un json con todos los juegos disponibles.
    # TODO Testing ->
    g_list = listing_games(SERVER_DB)

    return ResponseList(games_list=g_list)


@pre_game.post("/start_game/{id_game}")
async def start(id_game: int):
    """Empezar un juego."""

    # En caso de exito debe iniciar la partida posteriormente sera implementado.
    # Actualizar los datos de la partida para que no se siga listando como disponible para unirse.
    # Tiene que repartir las cartas a todos los jugadores.
    # Tiene que cambiar el estado a "Playing".
    # Tiene que inicializar el tablero randomizado.
    # Tiene que avisar a todos los clientes.
    players = get_players(id_game,SERVER_DB)
    if players >= get_min_players(id_game,SERVER_DB):
        
        set_game_state(id_game=id_game,
                       state="Playing",
                       db=SERVER_DB)
        
        first = set_users_turn(id_game=id_game,
                               players=players,
                               db=SERVER_DB)
        
        initialize_moves(id_game, players, SERVER_DB)
        initialize_figures(id_game, players ,SERVER_DB)
        PARTIAL_BOARDS.initialize(id_game,SERVER_DB)

        await manager.broadcast(f"GAME_STARTED {first}", id_game)
    
    else:
        raise HTTPException(status_code=409, detail="El lobby no alcanzo su capacidad minima para comenzar.")
    

    return {"message": "El juego comenzo correctamente."}
    

@pre_game.websocket("/ws/{id_game}/{user_id}")
async def websocket_endpoint(ws: WebSocket, id_game: int, user_id: int):
    """Canal para que el servidor envie datos de la partida."""
    await manager.connect(ws, id_game, user_id)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws, id_game, user_id)
