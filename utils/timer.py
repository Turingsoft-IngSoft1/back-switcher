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
KILL_APP = False
def handle_sigint(signum, frame):
    global KILL_APP
    KILL_APP = True
signal(SIGINT, handle_sigint)

class GameTimer:
    """Clase para manejar timers."""
    def __init__(self):
        self.start_time = None
        self.duration = 10

    def start(self):
        """Iniciar timer."""
        self.start_time = datetime.now(timezone.utc)
        
    def time_remaining(self):
        """Tiempo restante en el timer."""
        if not self.start_time:
            return 0
        time_passed = datetime.now(timezone.utc) - self.start_time
        return max(0, self.duration - int(time_passed.total_seconds()))

# Diccionario para almacenar los timers por ID de partida.
GAME_TIMERS: Dict[int, GameTimer] = {}

def initialize_timer(id_game: int):
    """Función para inicializar el timer."""
    if id_game not in GAME_TIMERS:
        GAME_TIMERS[id_game] = GameTimer()
        
async def start_timer(id_game: int):
    """Función para comenzar el timer."""
    if id_game in GAME_TIMERS:
        GAME_TIMERS[id_game].start()
        await manager.broadcast("TIMER_START", id_game)
                
def remove_timer(id_game: int):
    """Elimina el timer de la partida."""
    if id_game in GAME_TIMERS:
        del GAME_TIMERS[id_game]

async def timer_restart(id_game: int):
    """Salta el turno si el timer termina."""
    while id_game in GAME_TIMERS and (not KILL_APP):
        remaining_time = GAME_TIMERS[id_game].time_remaining()
        await manager.broadcast(f"TIMER {remaining_time}", id_game)
        await sleep(1)
        # Chequea que no se cierre el servidor en medio del ciclo.
        if KILL_APP:
            break
        elif remaining_time <= 0:
            await skip_turn(id_game)
            # Reinicia el temporizador y lanza un nuevo ciclo.
            await start_timer(id_game)
            
@staticmethod
async def skip_turn(id_game: int):
    actual_turn = get_game_turn(id_game, SERVER_DB)
    actual_players = get_players(id_game, SERVER_DB)
    new_turn = (actual_turn + 1) % actual_players
    set_game_turn(id_game, new_turn, SERVER_DB)
    id_user = get_user_from_turn(id_game, new_turn, SERVER_DB)
    await manager.broadcast(f"TURN {id_user}", id_game)
    unplay_moves(id_game, SERVER_DB)
    PARTIAL_BOARDS.remove(id_game)
    PARTIAL_BOARDS.initialize(id_game, SERVER_DB)
    await manager.broadcast("REFRESH_BOARD", id_game)