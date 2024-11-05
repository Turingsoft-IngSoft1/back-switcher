import pytest

from utils.timer import *
from unittest.mock import AsyncMock
from datetime import datetime, timedelta, timezone

@pytest.fixture(autouse=True)
async def cleanup():
    """Limpia el diccionario de timers antes y después de cada prueba."""
    game_timers.clear()  # Limpieza inicial
    yield
    game_timers.clear()  # Limpieza final

@pytest.mark.asyncio
async def test_time_remaining_decreases():
    """Inicializa y empieza el temporizador"""
    await initialize_timer(2)
    
    initial_time = game_timers[2].time_remaining()
    assert initial_time > 0

    await sleep(1)
    new_time = game_timers[2].time_remaining()
    
    assert new_time < initial_time
    assert new_time > 0 

@pytest.mark.asyncio
async def test_timer_reaches_zero():
    """Configura el temporizador con duración corta para pruebas"""
    game_timer = GameTimer()
    game_timer.duration = 1
    game_timers[3] = game_timer
    
    game_timers[3].start()
    await sleep(2) 
    
    assert game_timers[3].time_remaining() == 0
    assert 3 in game_timers
    
async def test_timer_loop_changes_turn(mocker):
    """Test para verificar que el turno se cambia cuando el tiempo se agota."""
    
    # Mockear las funciones necesarias
    mock_get_turn = mocker.patch('querys.game_queries.get_game_turn', return_value=1)
    mock_set_turn = mocker.patch('querys.game_queries.set_game_turn')
    mock_get_players = mocker.patch('querys.game_queries.get_players', return_value=4)  # Supongamos que hay 4 jugadores
    mock_get_user_from_turn = mocker.patch('querys.user_queries.get_user_from_turn', return_value=10)  # ID del usuario para el siguiente turno
    mock_broadcast = mocker.patch('utils.ws.manager.broadcast')
    
    # Inicializar el temporizador para el juego 1
    await initialize_timer(1)

    # Forzar que el tiempo restante sea 0
    game_timers[1].start_time = datetime.now(timezone.utc) - timedelta(seconds=121)  
    
    # Cambiar in_turn a True para simular que está en su turno
    game_timers[1].in_turn = True

    # Ejecuta el loop del temporizador
    await timer_loop(1)
    
    # Verifica que las funciones mockeadas fueron llamadas con los parámetros esperados
    mock_get_turn.assert_called_once_with(1, SERVER_DB)
    mock_set_turn.assert_called_once_with(1, 2, SERVER_DB)  # El turno cambia de 1 a 2
    mock_get_players.assert_called_once_with(1, SERVER_DB)
    mock_get_user_from_turn.assert_called_once_with(1, 2 % 4, SERVER_DB)  # Cambio de turno al jugador correcto
    mock_broadcast.assert_any_call(f"TURN {10}", 1)  # Verifica que se ha enviado el mensaje de turno
    mock_broadcast.assert_any_call("REFRESH_BOARD", 1)  # Verifica que se ha enviado la señal de refresco de tablero


@pytest.mark.asyncio
async def test_timer_loop(mocker):
    """Test para verificar el bucle de timer que envía actualizaciones."""
    mock_broadcast = mocker.patch.object(manager, 'broadcast')

    await initialize_timer(3)
    await sleep(1)
    mock_broadcast.assert_called()
    assert mock_broadcast.call_count > 0

    
    
def test_time_remaining_not_started():
    """Test para verificar el tiempo restante en un temporizador no iniciado."""
    # Inicializamos el temporizador
    timer = GameTimer()  # Crea una nueva instancia de GameTimer
    remaining_time = timer.time_remaining()  # Llama a time_remaining sin iniciar el temporizador
    assert remaining_time == 0  # Verifica que el tiempo restante sea 0
