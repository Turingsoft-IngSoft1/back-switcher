from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from querys.game_queries import *
from querys.user_queries import *
from querys.move_queries import *
from querys.figure_queries import *
from schemas.response_models import *
from querys import create_board, get_color
from utils.ws import manager, is_disconnected
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS
from utils.timer import initialize_timer, start_timer, timer_end
from utils.profiles import PROFILES

pre_game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@pre_game.get("/")
def default():
    """Mensaje predeterminado."""
    return "El Switcher."

@pre_game.get("/new_profile/")
def new_profile():
    profile_id: str = PROFILES.get_new_profile()
    return profile_id

@pre_game.get("/load_profile/{profile_id}", response_model=list[GamesData])
def load_games(profile_id: str):
    profile = PROFILES.get_games(profile_id)
    
    if profile is None:
        raise HTTPException(status_code=404, detail="No se encontro un perfil valido.")
    else:
        response = []
        for id_game, id_user in profile:
            if (g:=get_game(id_game, SERVER_DB)) and is_disconnected(id_game, id_user):
                response.append(GamesData(id_game=id_game,game_name=g.name,
                                          players=g.players,id_user=id_user,
                                          user_name=get_username(id_user, SERVER_DB)))
        return response

@pre_game.get("/recover_game_data/{id_game}/{id_user}", response_model=ActualGameData)
def get_game_actual_data(id_game: int, id_user: int):
    
    game = get_game(id_game, SERVER_DB)
    if game is None or game.state != "Playing":
        raise HTTPException(status_code=404, detail="La partida especificada no existe o todavia no comenzó.")
    
    users = uid_by_turns(id_game, SERVER_DB)
    current_turn = get_game_turn(id_game, SERVER_DB) % get_players(id_game, SERVER_DB)

    if id_user not in users:
        raise HTTPException(status_code=404, detail="El usuario no existe en la partida.")

    return ActualGameData(actual_board=PARTIAL_BOARDS.get(id_game),
                          blocked_color=get_color(id_game, SERVER_DB),
                          actual_turn_player=users[current_turn],
                          available_moves=get_hand(id_game, id_user, SERVER_DB),
                          partial_moves=get_partial_moves(id_game, id_user, SERVER_DB))

@pre_game.get("/active_players/{id_game}", response_model=CurrentUsers)
def get_active_players(id_game: int):
    """Devuelve los jugadors conectados a una partida."""
    return CurrentUsers(users_list=get_users(id_game=id_game,db=SERVER_DB))


@pre_game.post("/create_game", response_model=ResponseCreate)
def create(e: CreateEntry, profile_id: str = ""):
    """Crear el juego."""
    # En caso de exito se debe retornar {id_player,id_game}.
    # Se debe crear un game_schema.Game.
    # TODO Agregar TESTs ->
    
    if check_length_password(e.password):
        raise HTTPException(status_code=400, detail="La contraseña ingresada no cumple el minimo de caracteres.")
    
    new_id_game = create_game(name=e.game_name,
                              max_players=e.max_player,
                              min_players=e.min_player,
                              password=e.password,
                              db=SERVER_DB)
    
    new_id_user = create_user(name=e.owner_name,
                              id_game=new_id_game,
                              db=SERVER_DB)
    
    set_game_host(id_game=new_id_game,
                  host=new_id_user,
                  db=SERVER_DB)
    
    create_board(id_game=new_id_game,
                 db=SERVER_DB)
    
    PROFILES.add_game(profile_id, new_id_game, new_id_user)

    return ResponseCreate(id_game=new_id_game, id_player=new_id_user)


@pre_game.post("/join_game", response_model=ResponseJoin)
async def join(e: JoinEntry, profile_id: str = ""):
    """Unirse al juego."""

    # En caso de exito debe conectar al jugador con el servidor por WebSocket?.
    # Se deben aplicar todos los cambios a la estructura interna de la paritda.
    # TODO Testing ->
    if get_max_players(e.id_game,SERVER_DB) > get_players(e.id_game,SERVER_DB):
        if check_length_password(e.password):
            raise HTTPException(status_code=400, detail="La contraseña ingresada no cumple el minimo de caracteres.")
        
        if verify_password(e.id_game, e.password, SERVER_DB):
            add_player(id_game=e.id_game,
                       db=SERVER_DB)
            id_user = create_user(name=e.player_name,
                               id_game=e.id_game,
                               db=SERVER_DB)
            PROFILES.add_game(profile_id, e.id_game, id_user)
            await manager.broadcast(f"{id_user} JOIN",e.id_game)
        else:
            raise HTTPException(status_code=403, detail="Contraseña incorrecta.")
    else:
        raise HTTPException(status_code=409, detail="El lobby está lleno.")

    return ResponseJoin(new_player_id=id_user)


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
    # Tiene que inicializar el timer.
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
        initialize_figures(id_game, players, SERVER_DB)
        PARTIAL_BOARDS.initialize(id_game, SERVER_DB)
        
        #timer
        initialize_timer(id_game)
        await start_timer(id_game)
        

        await manager.broadcast(f"GAME_STARTED {first}", id_game)
        
        await timer_end(id_game)
    
    else:
        raise HTTPException(status_code=409, detail="El lobby no alcanzo su capacidad minima para comenzar.")
    

    return {"message": "El juego comenzo correctamente."}


@pre_game.post("/cancel_game/{id_game}/{id_caller}")
async def cancel_game(id_game: int, id_caller: int):
    """Eliminar la partida si el host la abandona antes de comenzar."""
    game = get_game(id_game, SERVER_DB)
    if game is None or game.state == "Playing":
        raise HTTPException(status_code=404, detail="La partida especificada no existe o ya comenzó.")
    elif id_caller != game.host:
        raise HTTPException(status_code=403, detail="El usuario no es el host de la partida.")

    await manager.broadcast("CANCELLED", id_game)
    remove_game(id_game, SERVER_DB)
    return {"Partida cancelada exitosamente"}


@pre_game.websocket("/ws/{id_game}/{id_user}")
async def websocket_endpoint(ws: WebSocket, id_game: int, id_user: int):
    """Canal para que el servidor envie datos de la partida."""
    await manager.connect(ws, id_game, id_user)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(id_game, id_user)

