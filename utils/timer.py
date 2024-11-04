from datetime import datetime, timezone
from typing import Dict
from utils.ws import manager
from asyncio import sleep

class GameTimer:
    """Clase para manejar timers."""
    def __init__(self):
        self.start_time = None
        self.duration = 120

    def start(self):
        """Iniciar timer."""
        self.start_time = datetime.now(timezone.utc)

    def time_remaining(self):
        """Tiempor restante en el timer."""
        if not self.start_time:
            return 0
        time_passed = datetime.now(timezone.utc) - self.start_time
        return max(0, self.duration - int(time_passed.total_seconds()))
    
# Diccionario para almacenar los temporizadores por ID de partida
game_timers: Dict[int, GameTimer] = {}

def initialize_timer(id_game: int):
    """Función para inicializar el temporizador para un juego específico."""
    if id_game not in game_timers:
        game_timer = GameTimer()
        game_timers[id_game] = game_timer

async def timer_loop(id_game: int):
    """Función asincrónica para enviar el tiempo restante en un bucle."""
    while id_game in game_timers:
        remaining_time = game_timers[id_game].time_remaining()
        await manager.broadcast(f"Time remaining: {remaining_time} seconds.")
        await sleep(1)
        if remaining_time <= 0:
            break