from datetime import datetime, timezone
from typing import Dict
from utils.ws import manager
from utils.database import SERVER_DB
from utils.partial_boards import PARTIAL_BOARDS
from asyncio import sleep, create_task, Lock
from querys.game_queries import get_players, get_game_turn, set_game_turn
from querys.user_queries import get_user_from_turn
from querys.move_queries import unplay_moves

class GameTimer:
    """Clase para manejar timers."""
    def __init__(self):
        self.start_time = None
        self.duration = 10
        self.is_running = False

    def start(self):
        """Iniciar timer."""
        self.start_time = datetime.now(timezone.utc)
        self.is_running = True
        
    def stop(self):
        self.start_time = None
        self.is_running = False

    def time_remaining(self):
        """Tiempo restante en el timer."""
        if not self.start_time:
            return 0
        time_passed = datetime.now(timezone.utc) - self.start_time
        return max(0, self.duration - int(time_passed.total_seconds()))

# Diccionario para almacenar los timers por ID de partida.
game_timers: Dict[int, GameTimer] = {}

def initialize_timer(id_game: int):
    """Función para inicializar el timer."""
    if id_game not in game_timers:
        game_timers[id_game] = GameTimer()
        
async def start_timer(id_game: int):
    """Función para comenzar el timer."""
    if id_game in game_timers:
        game_timers[id_game].start()
        await manager.broadcast("TIMER_START", id_game)
    
async def stop_timer(id_game: int):
    """Función para detener el timer."""
    if id_game in game_timers:
        game_timers[id_game].stop()
        await manager.broadcast("TIMER_STOP", id_game)
                
def remove_timer(id_game: int):
    """Elimina el timer de la partida."""
    if id_game in game_timers:
        del game_timers[id_game]
        
def timer_is_running(id_game: int):
    """Verfica que el timer este corriendo."""
    if id_game in game_timers:
        return game_timers[id_game].is_running


async def timer_end(id_game: int):
    """Salta el turno si el timer termina."""
    while id_game in game_timers:
        remaining_time = game_timers[id_game].time_remaining()
        await manager.broadcast(f"{remaining_time} seconds.", id_game)
        await sleep(1)
        if not timer_is_running(id_game):
            break
        if remaining_time <= 0:
            actual_turn = get_game_turn(id_game, SERVER_DB)
            actual_players = get_players(id_game, SERVER_DB)
            set_game_turn(id_game, (actual_turn + 1), SERVER_DB)
            game_turn = (get_game_turn(id_game, SERVER_DB) % actual_players)
            id_user = get_user_from_turn(id_game, game_turn, SERVER_DB)
            await manager.broadcast(f"TURN {id_user}", id_game)
            unplay_moves(id_game, SERVER_DB)
            PARTIAL_BOARDS.remove(id_game)
            PARTIAL_BOARDS.initialize(id_game, SERVER_DB)
            await manager.broadcast("REFRESH_BOARD", id_game)

            # Reinicia el temporizador y lanza un nuevo ciclo
            await stop_timer(id_game)
            await start_timer(id_game)
            
            break
    await timer_end(id_game)