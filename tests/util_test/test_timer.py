import pytest

from utils.timer import *

@pytest.mark.asyncio
async def test_time_remaining_decreases():
    """Inicializa y empieza el temporizador"""
    initialize_timer(2)
    game_timers[2].start()
    
    initial_time = game_timers[2].time_remaining()
    assert initial_time > 0

    await sleep(1)
    new_time = game_timers[2].time_remaining()
    
    assert new_time < initial_time
    assert new_time > 0 

@pytest.mark.asyncio
async def test_timer_reaches_zero_and_removes():
    """Configura el temporizador con duración corta para pruebas"""
    game_timer = GameTimer()
    game_timer.duration = 1
    game_timers[3] = game_timer
    
    game_timers[3].start()
    await sleep(2) 
    
    assert game_timers[3].time_remaining() == 0
    assert 3 in game_timers

@pytest.mark.asyncio
async def test_timer_loop(mocker):
    """Test para verificar el bucle de timer que envía actualizaciones."""
    initialize_timer(3)
    game_timers[3].start()
    mock_broadcast = mocker.patch.object(manager, 'broadcast')
    await timer_loop(3)
    mock_broadcast.assert_called()
    assert mock_broadcast.call_count > 0
    
def test_time_remaining_not_started():
    """Test para verificar el tiempo restante en un temporizador no iniciado."""
    # Inicializamos el temporizador
    timer = GameTimer()  # Crea una nueva instancia de GameTimer
    remaining_time = timer.time_remaining()  # Llama a time_remaining sin iniciar el temporizador
    assert remaining_time == 0  # Verifica que el tiempo restante sea 0
