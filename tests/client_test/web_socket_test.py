"""
import asyncio
import pytest
from starlette.testclient import TestClient
from main import app

@pytest.mark.asyncio
async def test_websocket_with_event(client,mock_server_db):
    
    with client.websocket_connect("/ws/1/1") as websocket:
        async def send_signal():
            await asyncio.sleep(1)
            response = client.post("http://localhost:8000/start_game/1")
            assert response.status_code == 200

        asyncio.create_task(send_signal())

        try:
            print("Waiting for WebSocket message...")
            response_message = await asyncio.wait_for(websocket.receive_text(), timeout=10)
            print(f"Received WebSocket message: {response_message}")
            assert response_message == "GAME_STARTED"
        except asyncio.TimeoutError:
            pytest.fail("El WebSocket no envió un mensaje en el tiempo esperado.")
        except Exception as e:
            pytest.fail(f"Ocurrió un error inesperado: {str(e)}")
"""