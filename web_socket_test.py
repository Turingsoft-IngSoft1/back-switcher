"""import pytest
import asyncio
import websockets
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_websocket():
    async with websockets.connect("ws://127.0.0.1:8000/ws/1") as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        assert response == "You wrote: Hello, WebSocket!"
        
        # Test broadcasting
        await websocket.send("Broadcast message")
        response = await websocket.recv()
        assert response == "Client #1 says: Broadcast message"



if __name__ == "__main__":
    
    asyncio.run(test_websocket())

"""