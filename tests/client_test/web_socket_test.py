"""import asyncio
import httpx
import pytest
import unittest

from main import app


class TestWS(unittest.TestCase):
    @pytest.mark.order(7)
    @pytest.mark.asyncio
    async def test_websocket_with_event(self):
        async with httpx.AsyncClient(app=app, base_url="http://test") as client:
            async with client.websocket_connect("/ws/1/1") as websocket:
                async def send_signal():
                    await asyncio.sleep(1)
                    async with httpx.AsyncClient() as other_client:
                        await other_client.post("https://localhost:8000/start_game/1")

                asyncio.create_task(send_signal())
        try:
            response_message = await asyncio.wait_for(websocket.receive_text(), timeout=4)
            self.assertEqual(response_message, "GAME_STARTED")
        except asyncio.TimeoutError:
            pytest.fail("El WebSocket no envió un mensaje en el tiempo esperado.")
        except Exception as e:
            pytest.fail(f"Ocurrió un error inesperado: {str(e)}")


if __name__ == '__main__':
    unittest.main()
"""