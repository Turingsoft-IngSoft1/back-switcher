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
        self.duration = 120
        self.is_running = False

    def start(self):
        """Iniciar timer."""
        self.start_time = datetime.now(timezone.utc)
        self.is_running = True
        
    def stop(self):
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
    """Función para inicializar el temporizador para un juego específico."""
    if id_game not in game_timers:
        game_timers[id_game] = GameTimer()
        
        
def start_timer(id_game: int):
    if id_game in game_timers:
        game_timers[id_game].start()
        
        # Inicia el loop del temporizador si no está en ejecución
        if not getattr(game_timers[id_game], "timer_task", None):
            game_timers[id_game].timer_task = create_task(timer_loop(id_game))
    
    

    
async def stop_timer(id_game: int):
    """Función para detener el timer."""
    if id_game in game_timers:
        game_timers[id_game].stop()
        if getattr(game_timers[id_game], "timer_task", None):
            task = game_timers[id_game].timer_task
            task.cancel()  # Cancelamos la tarea

            # Comprobar si la tarea no ha sido cancelada y esperar su finalización
            if not task.done():
                await task


async def timer_loop(id_game: int):
    """Función asincrónica para enviar el tiempo restante en un bucle."""
    while id_game in game_timers:
        remaining_time = game_timers[id_game].time_remaining()
        await manager.broadcast(f"{remaining_time} seconds.", id_game)
        await sleep(120)
        if not game_timers[id_game].is_running:
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
            await initialize_timer(id_game)
            break