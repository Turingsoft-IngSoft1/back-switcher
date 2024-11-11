import pytest

from utils.timer import *
from unittest.mock import AsyncMock
from datetime import datetime, timedelta, timezone

@pytest.fixture(autouse=True)
async def cleanup():
    """Limpia el diccionario de timers antes y después de cada prueba."""
    GAME_TIMERS.clear()  # Limpieza inicial
    yield
    GAME_TIMERS.clear()  # Limpieza final

@pytest.mark.asyncio
async def test_time_remaining_decreases():
    """Inicializa y empieza el temporizador"""
    initialize_timer(2)
    start_timer(2)
    
    initial_time = GAME_TIMERS[2].time_remaining()
    assert initial_time > 0

    await sleep(1)
    new_time = GAME_TIMERS[2].time_remaining()
    
    assert new_time < initial_time
    assert new_time > 0 

@pytest.mark.asyncio
async def test_timer_reaches_zero():
    """Configura el temporizador con duración corta para pruebas"""
    game_timer = GameTimer()
    game_timer.duration = 1
    GAME_TIMERS[3] = game_timer
    
    GAME_TIMERS[3].start()
    await sleep(2) 
    
    assert GAME_TIMERS[3].time_remaining() == 0
    assert 3 in GAME_TIMERS
    
@pytest.mark.asyncio
async def test_timer_loop_changes_turn(test_db, mocker):
    # Preparar el entorno para el juego con un ID de prueba.
    id_game = 1
    
    # Crear mocks para las funciones necesarias.
    mocker.patch("querys.game_queries.get_game_turn", side_effect=[1, 2])  # El turno inicial es 1, luego 2
    mocker.patch("querys.game_queries.get_players", return_value=2)        # Total de jugadores es 2
    mock_set_game_turn = mocker.patch("querys.game_queries.set_game_turn") # Mock para verificar cambio de turno
    mocker.patch("querys.game_queries.set_game_turn")
    mocker.patch("querys.user_queries.get_user_from_turn", return_value=1) 
    mocker.patch("querys.move_queries.unplay_moves")
    mocker.patch("utils.partial_boards.PARTIAL_BOARDS.remove")
    mocker.patch("utils.partial_boards.PARTIAL_BOARDS.initialize")

    # Inicializar y empezar el temporizador para el juego.
    initialize_timer(id_game)
    start_timer(id_game)
    
    # Espera para permitir que `timer_loop` cambie el turno.
    await sleep(3)
    
    # Comprobar que el turno fue actualizado correctamente.
    mock_set_game_turn.assert_called_with(id_game, 2, test_db)
    
    # Asegurarse de que el temporizador esté corriendo.
    assert GAME_TIMERS[id_game].is_running
    
    # Detener el temporizador al final para limpiar.

@pytest.mark.asyncio
async def test_timer_loop(mocker):
    """Test para verificar el bucle de timer que envía actualizaciones."""
    mock_broadcast = mocker.patch.object(manager, 'broadcast')

    initialize_timer(3)
    start_timer(3)
    await sleep(1)
    mock_broadcast.assert_called()
    assert mock_broadcast.call_count > 0

    
    
def test_time_remaining_not_started():
    """Test para verificar el tiempo restante en un temporizador no iniciado."""
    # Inicializamos el temporizador
    timer = GameTimer()  # Crea una nueva instancia de GameTimer
    remaining_time = timer.time_remaining()  # Llama a time_remaining sin iniciar el temporizador
    assert remaining_time == 0  # Verifica que el tiempo restante sea 0
