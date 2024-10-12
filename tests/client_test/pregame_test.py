import json,pytest
from unittest.mock import patch

def test_create_game(client):
    #Crear PartidaEjemplo y UsuarioEjemplo. 
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 3,
        "max_player": 4
    }
    response = client.post(url, json=payload)
    assert response.status_code == 200
    #Intento crear PartidaErronea.
    payload = {
        "game_name": "PartidaErronea",
        "owner_name": "UsuarioErroneo",
        "min_player": 2,
        "max_player": 1
    }
    response = client.post(url, json=payload)
    assert response.status_code == 422

def test_list_game(client):
    #Crear PartidaEjemplo y UsuarioEjemplo. 
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 3,
        "max_player": 4
    }
    response = client.post(url, json=payload)
    #Listar partidas, solo deberia aparecer PartidaEjemplo.
    url = "http://localhost:8000/list_games"
    expected_json = {
        "games_list": [
            {
                "id": 1,
                "name": "PartidaEjemplo",
                "state": "Waiting",
                "turn": 0,
                "host": 1,
                "players": 1,
                "max_players": 4,
                "min_players": 3,
                "password": "password"
            }
        ]
    }
    response = client.get(url)
    formatted_response = json.dumps(response.json(), sort_keys=True)
    formatted_expected = json.dumps(expected_json, sort_keys=True)
    assert response.status_code == 200
    assert formatted_expected, formatted_response

def test_join_game(client):
    #Crear PartidaEjemplo y UsuarioEjemplo. 
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 3,
        "max_player": 4
    }
    response = client.post(url, json=payload)
    #Unir a UsuarioUnido a la partida.
    url = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioUnido"
    }

    expected_json = {
        "new_player_id": 2
    }

    response = client.post(url, json=payload)
    assert response.status_code == 200
    formatted_response = json.dumps(response.json(), sort_keys=True)
    formatted_expected = json.dumps(expected_json, sort_keys=True)
    assert formatted_expected == formatted_response

def test_active_players(client):
    #Crear PartidaEjemplo y UsuarioEjemplo.    
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2
    }
    response = client.post(url, json=payload)
    #Listar jugadores activos en el juego con id 1.
    url = "http://localhost:8000/active_players/1"
    response = client.get(url)
    expected_json = {
        "users_list": [
            {
                "id": 1,
                "name": "UsuarioEjemplo",
                "game": 1,
                "figures_deck": 13,
                "turn": 0
            }
        ]
    }
    assert response.status_code == 200
    formatted_expected = json.dumps(response.json(), sort_keys=True)
    formatted_response = json.dumps(response.json(), sort_keys=True)
    assert formatted_expected == formatted_response

def test_start_game(client):
    #Crear partida y jugador 1.    
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2
    }
    response = client.post(url, json=payload)
    #Inteto errorneo de iniciar partida.
    url = "http://localhost:8000/start_game/1"
    response = client.post(url)
    error_json = {
        "detail": "El lobby no alcanzo su capacidad minima para comenzar."
    }
    assert response.status_code == 409
    formatted_response = json.dumps(response.json(), sort_keys=True)
    formatted_error = json.dumps(error_json, sort_keys=True)
    assert formatted_response == formatted_error
    #Unir a jugador2 para poder iniciar partida.
    urljoin = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby"
    }
    client.post(urljoin, json=payload)
    #Se inicia partida correctamente.
    response = client.post(url)
    expected_json = {
        "message": "El juego comenzo correctamente."
    }
    assert response.status_code == 200
    formatted_response = json.dumps(response.json(), sort_keys=True)
    formatted_expected = json.dumps(expected_json, sort_keys=True)
    assert formatted_response == formatted_expected

