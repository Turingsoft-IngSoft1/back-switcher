from typing import  Dict
from fastapi import APIRouter,HTTPException,WebSocket,WebSocketDisconnect
from querys.game_queries import *
from querys.user_queries import *
from querys import get_board,get_revealed_figures,unplay_moves, get_blocked_figures, get_color
from schemas.response_models import InGame,BoardStatus,UserData
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS
from utils.boardDetect import detect_figures
from utils.profiles import PROFILES
game = APIRouter()


# Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
async def leave(e: InGame, profile_id: str = ""):
    """Abandonar Partida."""
    # En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    if is_user_current_turn(e.id_game, e.id_player, SERVER_DB):
        remove_player(e.id_game,SERVER_DB)
        remove_user(e.id_player,SERVER_DB)
        reorder_turns(e.id_game,SERVER_DB)
        await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)
        
        set_game_turn(e.id_game, (get_game_turn(e.id_game,SERVER_DB) + 1),SERVER_DB)
        game_turn = (get_game_turn(e.id_game,SERVER_DB) % (get_players(e.id_game,SERVER_DB)))
        id_user = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
        await manager.broadcast(f"TURN {id_user}", e.id_game)

        
    
    else:
        remove_player(e.id_game,SERVER_DB)
        remove_user(e.id_player,SERVER_DB)
        reorder_turns(e.id_game,SERVER_DB)
        await manager.broadcast(f"{e.id_player} LEAVE", e.id_game)

    #Ganar por abando.
    if get_players(e.id_game,SERVER_DB) == 1 and get_game_state(e.id_game,SERVER_DB) == "Playing":
        set_game_state(e.id_game, "Finished", SERVER_DB)
        winner = get_users(e.id_game,SERVER_DB)
        await manager.broadcast(f"{winner[0].id} WIN", e.id_game)

    #Cuando no queda ningun jugador se elimina partida.
    if get_players(e.id_game,SERVER_DB) == 0:
        remove_game(e.id_game,SERVER_DB)
        PARTIAL_BOARDS.remove(e.id_game)

    PROFILES.remove_game(profile_id,e.id_game,e.id_player)
    
    return {"message": "Exit Successful."}


@game.post("/skip_turn")
async def skip(e: InGame):
    """Pasar el turno."""
    
    # En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.
    actual_turn = get_game_turn(e.id_game,SERVER_DB)
    actual_players = get_players(e.id_game,SERVER_DB)
    set_game_turn(e.id_game, (actual_turn + 1),SERVER_DB)
    game_turn = (get_game_turn(e.id_game,SERVER_DB) % actual_players)
    id_user = get_user_from_turn(e.id_game,game_turn,SERVER_DB)
    await manager.broadcast(f"TURN {id_user}", e.id_game)
    unplay_moves(e.id_game,SERVER_DB)
    PARTIAL_BOARDS.remove(e.id_game)
    PARTIAL_BOARDS.initialize(e.id_game, SERVER_DB)
    await manager.broadcast("REFRESH_BOARD", e.id_game)

    return {"Skip Successful."}

#TODO test
@game.get("/game_status/{id_game}",response_model=list[UserData])
async def get_status(id_game: int):
    """Consultar estado de partida/turnos."""
    fa = get_revealed_figures(id_game, SERVER_DB)
    fb = get_blocked_figures(id_game, SERVER_DB)
    users = get_users(id_game, SERVER_DB)
    response = []
    for u in users:
        response.append(UserData(id_user=u.id,
                                 name=u.name,
                                 figures_available=fa[u.id],
                                 figures_blocked=fb[u.id]))
    return response


@game.get("/board_status/{id_game}", response_model=BoardStatus)
async def get_board_status(id_game: int):
    """Consultar estado del tablero."""
    if get_game(id_game=id_game,db=SERVER_DB) is not None:
        return BoardStatus(board=get_board(id_game=id_game, db=SERVER_DB),
                           blocked_color=get_color(id_game=id_game, db=SERVER_DB))
    else:
        raise HTTPException(status_code=404, detail=f"El juego con id_game={id_game} no existe.")

#TODO test
@game.get("/detect_figures_on_board/{id_game}/{id_user}")
async def detect_figures_on_board(id_game: int, id_user: int):
    if (g := get_game(id_game=id_game, db=SERVER_DB)) is not None and (g.state == "Playing"):
        if id_user in uid_by_turns(id_game,SERVER_DB):
            rf = get_revealed_figures(id_game,SERVER_DB)
            figures =  set(item for sublist in rf.values() for item in sublist)
            detected_figures = detect_figures(PARTIAL_BOARDS.get(id_game),figures)
            # [0]: color, [1]: figura, [2]: lista de coordenadas
            response: Dict[str, Dict[str, list]] = {}
            for detected_fig in detected_figures:
                if detected_fig[1] not in response:
                    response[detected_fig[1]] = {}
                if detected_fig[0] not in response[detected_fig[1]]:
                    response[detected_fig[1]][detected_fig[0]] = []
                response[detected_fig[1]][detected_fig[0]].append(detected_fig[2])
            return response

        else:
            raise HTTPException(status_code=404,
                                detail=f"El usuario con id_user={id_user} no existe en la partida.")
    else:
        raise HTTPException(status_code=404,
                            detail=f"El juego con id_game={id_game} no existe o todavia no comenzo.")
    

@game.websocket("/chat/{id_game}/{id_user}")
async def websocket_endpoint(ws: WebSocket, id_game: int, id_user: int):
    """Canal para que el servidor envie datos de la partida."""
    await manager.connect(ws, id_game, id_user, 'chat') #pragma: no cover
    try:
        while True:
            await ws.receive_text() #pragma: no cover
    except WebSocketDisconnect:
        manager.disconnect(id_game, id_user, 'chat') #pragma: no cover

@game.post("/chat/{id_game}/{id_user}")
async def send_message_chat(id_game: int, id_user: int, message: str):
    """Enviar mensaje de chat."""
    game = get_game(id_game=id_game, db=SERVER_DB)
    if not game:
        raise HTTPException(status_code=404, detail=f"El juego con id_game={id_game} no existe.")

    users = uid_by_turns(id_game, SERVER_DB)
    if id_user not in users:
        raise HTTPException(status_code=404, detail=f"El usuario con id_user={id_user} no existe en la partida.")

    recipient_users = [user for user in users if user != id_user]
    sender_name = get_username(id_user, SERVER_DB)

    for user in recipient_users:
        await manager.send_personal_message(f"{sender_name}: {message}", id_game, user, 'chat')

    return {"message": "Message sent."}
