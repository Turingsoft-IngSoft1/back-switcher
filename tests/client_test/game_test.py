import json,pytest
from unittest.mock import patch
from querys.board_queries import update_board
from utils.timer import game_timers

def test_leave(client):
    #Crear PartidaEjempo y UsuarioEjemplo. 
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 4,
        "password": ""
    }
    client.post(url_create, json=payload)
    #Unir a UsuarioParaLlenarLobby a la partida.
    urljoin = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby",
        "password": ""
    }
    client.post(urljoin, json=payload)
    #Abandona UsuarioEjemplo
    url = "http://localhost:8000/leave_game"
    payload = {
        "id_player": 1,
        "id_game": 1
    }
    response = client.post(url, json=payload)
    expected_json = {
        "message": "Exit Successful."
    }
    assert response.status_code == 200
    formatted_response = json.dumps(response.json(), sort_keys=True)
    formatted_expected = json.dumps(expected_json, sort_keys=True)
    assert formatted_response == formatted_expected
    #Abandona UsuarioParaLlenarLobby
    payload = {
        "id_player": 1,
        "id_game": 1
    }
    client.post(url, json=payload)
    #Chequear que partida vacia se elemina.
    url_list = "http://localhost:8000/list_games"
    response=client.get(url_list)
    assert response.status_code == 200
    expected_json = {
        "games_list": []
    }
    formatted_response = json.dumps(response.json(), sort_keys=True)
    formatted_expected = json.dumps(expected_json, sort_keys=True)
    assert formatted_response == formatted_expected

def test_skip_turn(client):
    #Crear PartidaEjempo y UsuarioEjemplo. 
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaTurnos",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2,
        "password": ""
    }
    client.post(url_create, json=payload)
    #Crear PartidaEjemplo y UsuarioEjemplo.    
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2
    }
    client.post(url_create, json=payload)
    
    #Unir a jugador2 para poder iniciar partida.
    url_join = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby"
    }
    client.post(url_join, json=payload)
    
    #Se inicia la partida.
    url_start = "http://localhost:8000/start_game/1"
    client.post(url_start)
    
    #Saltear turno actuala de la PartidaEjemplo.
    url = "http://localhost:8000/skip_turn"
    payload = {
      "id_player": 1,
      "id_game": 1
    }
    response = client.post(url, json=payload)
    assert response.status_code == 200

#TODO agregar caso de test cuando este el endpoint de bloquear figuras.
def test_get_status(test_db, client):
    #Crear PartidaEjempo y UsuarioEjemplo. 
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2,
        "password": ""
    }
    client.post(url_create, json=payload)
    
    #Unir a UsuarioParaLlenarLobby a la partida.
    urljoin = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby",
        "password": ""
    }
    client.post(urljoin, json=payload)
    
    #Se inicia la partida.
    url_start = "http://localhost:8000/start_game/1"
    client.post(url_start)
    
    #Obtener el status de la partida.
    url_status = "http://localhost:8000/game_status/1"
    response = client.get(url_status)
    
    assert response.status_code == 200
    
    response_data = response.json()
    
    assert isinstance(response_data, list)
    for user in response_data:
        assert "id_user" in user
        assert "name" in user
        assert "figures_available" in user
        assert "figures_blocked" in user

        if user["id_user"] == 1:
            assert len(user["figures_available"]) == 3
            assert len(user["figures_blocked"]) == 0
        elif user["id_user"] == 2:
            assert len(user["figures_available"]) == 3
            assert len(user["figures_blocked"]) == 0
    
def test_get_board_status(test_db, client):
    #Crear PartidaEjempo y UsuarioEjemplo. 
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaTurnos",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2,
        "password": ""
    }
    client.post(url_create, json=payload)
    
    sucess=[['R','R','R','R','R','R'],
            ['R','R','R','G','G','G'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    expected_json = {"board":sucess, "blocked_color": "NOT"}
    update_board(1,sucess,test_db)

    url_board= "http://localhost:8000/board_status/1"
    
    response=client.get(url_board)
    
    formatted_expected = json.dumps(expected_json, sort_keys=True)
    formatted_response = json.dumps(response.json(), sort_keys=True)
    
    assert response.status_code == 200
    assert formatted_response == formatted_expected    

    url_board= "http://localhost:8000/board_status/2"
    response=client.get(url_board)
    assert response.status_code == 404