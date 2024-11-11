import pytest
from utils.timer import *

@pytest.fixture(autouse=True)
async def cleanup():
    """Limpia el diccionario de timers antes y después de cada prueba."""
    GAME_TIMERS.clear()  # Limpieza inicial
    yield
    GAME_TIMERS.clear()  # Limpieza final

@pytest.mark.asyncio
async def test_time_remaining_decreases():
    """Verifica que el tiempo restante en el timer disminuye."""
    initialize_timer(2)
    await start_timer(2)
    
    initial_time = GAME_TIMERS[2].time_remaining()
    assert initial_time > 0

    await sleep(1)
    new_time = GAME_TIMERS[2].time_remaining()
    
    assert new_time < initial_time
    assert new_time > 0

@pytest.mark.asyncio
async def test_timer_reaches_zero():
    """Verifica que el timer llegue a cero."""
    game_timer = GameTimer()
    game_timer.duration = 1
    GAME_TIMERS[3] = game_timer
    
    GAME_TIMERS[3].start()
    await sleep(2) 
    
    assert GAME_TIMERS[3].time_remaining() == 0
    assert 3 in GAME_TIMERS

@pytest.mark.asyncio
async def test_timer_loop_broadcast_updates(mocker):
    """Test para verificar el bucle de timer y las actualizaciones de broadcast."""
    mock_broadcast = mocker.patch.object(manager, 'broadcast')

    initialize_timer(3)
    await start_timer(3)
    await sleep(1)
    
    # Asegura que se llame al broadcast para las actualizaciones del temporizador
    assert mock_broadcast.call_count > 0
    mock_broadcast.assert_called_with("TIMER_START", 3)

def test_time_remaining_not_started():
    """Test para verificar el tiempo restante en un temporizador no iniciado."""
    timer = GameTimer()
    remaining_time = timer.time_remaining()
    assert remaining_time == 0