import json, pytest
from unittest.mock import patch

def test_get_moves(mock_server_db,test_db,client,force_teardown):
    #Crear PartidaEjemplo y UsuarioEjemplo.    
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2
    }
    client.post(url, json=payload)
    
    #Unir a jugador2 para poder iniciar partida.
    urljoin = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby"
    }
    client.post(urljoin, json=payload)
    
    #Se inicia la partida.
    url = "http://localhost:8000/start_game/1"
    client.post(url)
    
    #Se le reparten movimientos correctamente al usuario 1.
    urlmoves = "http://localhost:8000/get_moves/1/1"
    response = client.post(urlmoves, json=payload)
    assert response.status_code == 200
    player1_moves = response.json()
    assert len(player1_moves) > 0  #Verifica que se reparten movimientos al jugador 1.
    
    #Se le reparten movimientos correctamente al usuario 2.
    urlmoves = "http://localhost:8000/get_moves/1/2"
    response = client.post(urlmoves, json=payload)
    assert response.status_code == 200
    player2_moves = response.json()
    assert len(player2_moves) > 0  #Verifica que se reparten movimientos al jugador 2.

#def test_use_moves(mock_server_db,test_db,client,force_teardown):

#def test_get_figures(mock_server_db,test_db,client,force_teardown):

#def test_use_figures(mock_server_db,test_db,client,force_teardown):