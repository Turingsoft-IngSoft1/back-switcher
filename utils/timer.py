from signal import signal, SIGINT
from datetime import datetime, timezone
from typing import Dict
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS
from asyncio import sleep
from querys.game_queries import get_players, get_game_turn, set_game_turn
from querys.user_queries import get_user_from_turn
from querys.move_queries import unplay_moves

#Controla que cuando se cierre el serividor no quede un loop
KILL_APP = False #pragma: no cover
def handle_sigint(signum, frame): #pragma: no cover
    global KILL_APP #pragma: no cover
    KILL_APP = True #pragma: no cover
signal(SIGINT, handle_sigint) #pragma: no cover

class GameTimer:
    """Clase para manejar timers."""
    def __init__(self): #pragma: no cover
        self.start_time = None #pragma: no cover
        self.duration = 120 #pragma: no cover

    def start(self): #pragma: no cover
        """Iniciar timer."""
        self.start_time = datetime.now(timezone.utc) #pragma: no cover
        
    def time_remaining(self): #pragma: no cover
        """Tiempo restante en el timer."""
        if not self.start_time: #pragma: no cover
            return 0 #pragma: no cover
        time_passed = datetime.now(timezone.utc) - self.start_time #pragma: no cover
        return max(0, self.duration - int(time_passed.total_seconds())) #pragma: no cover

# Diccionario para almacenar los timers por ID de partida.
GAME_TIMERS: Dict[int, GameTimer] = {} #pragma: no cover

def initialize_timer(id_game: int): #pragma: no cover
    """Función para inicializar el timer."""
    if id_game not in GAME_TIMERS: #pragma: no cover
        GAME_TIMERS[id_game] = GameTimer() #pragma: no cover
        
async def start_timer(id_game: int): #pragma: no cover
    """Función para comenzar el timer."""
    if id_game in GAME_TIMERS: #pragma: no cover
        GAME_TIMERS[id_game].start() #pragma: no cover
                
def remove_timer(id_game: int): #pragma: no cover
    """Elimina el timer de la partida."""
    if id_game in GAME_TIMERS: #pragma: no cover
        del GAME_TIMERS[id_game] #pragma: no cover

async def restart_timer(id_game: int): #pragma: no cover
    """Salta el turno si el timer termina."""
    while id_game in GAME_TIMERS and (not KILL_APP): #pragma: no cover
        remaining_time = GAME_TIMERS[id_game].time_remaining() #pragma: no cover
        await manager.broadcast(f"TIMER {remaining_time}", id_game) #pragma: no cover
        await sleep(1) #pragma: no cover
        # Chequea que no se cierre el servidor en medio del ciclo.
        if KILL_APP: #pragma: no cover
            break
        elif remaining_time <= 0: #pragma: no cover
            await skip_turn(id_game) #pragma: no cover
            # Reinicia el temporizador y lanza un nuevo ciclo.
            await start_timer(id_game) #pragma: no cover
            
@staticmethod
async def skip_turn(id_game: int): #pragma: no cover
    actual_turn = get_game_turn(id_game, SERVER_DB) #pragma: no cover
    actual_players = get_players(id_game, SERVER_DB) #pragma: no cover
    new_turn = (actual_turn + 1) % actual_players #pragma: no cover
    set_game_turn(id_game, new_turn, SERVER_DB) #pragma: no cover
    id_user = get_user_from_turn(id_game, new_turn, SERVER_DB) #pragma: no cover
    await manager.broadcast(f"TURN {id_user}", id_game) #pragma: no cover
    unplay_moves(id_game, SERVER_DB) #pragma: no cover
    PARTIAL_BOARDS.remove(id_game) #pragma: no cover
    PARTIAL_BOARDS.initialize(id_game, SERVER_DB) #pragma: no cover
    await manager.broadcast("REFRESH_BOARD", id_game) #pragma: no cover