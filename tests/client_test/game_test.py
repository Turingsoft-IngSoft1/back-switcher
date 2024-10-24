import json,pytest
from unittest.mock import patch
from querys.board_queries import update_board

def test_leave(client):
    #Crear PartidaEjempo y UsuarioEjemplo. 
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 4
    }
    client.post(url_create, json=payload)
    #Unir a UsuarioParaLlenarLobby a la partida.
    urljoin = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby"
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
        "max_player": 2
    }
    client.post(url_create, json=payload)
    #Saltear turno actuala de la PartidaEjemplo.
    url = "http://localhost:8000/skip_turn"
    payload = {
      "id_player": 1,
      "id_game": 1
    }
    response = client.post(url, json=payload)
    assert response.status_code == 200

def test_get_board_status(test_db,client):
    #Crear PartidaEjempo y UsuarioEjemplo. 
    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaTurnos",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2
    }
    client.post(url_create, json=payload)
    
    sucess=[['R','R','R','R','R','R'],
            ['R','R','R','G','G','G'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    expected_json = {"board":sucess}
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
