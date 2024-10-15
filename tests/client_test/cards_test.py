from pytest import MonkeyPatch
import json
from querys import uid_by_turns

def test_get_moves(client):
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
    
    #Se le reparten movimientos correctamente al usuario 1.
    url_moves = "http://localhost:8000/get_moves/1/1"
    response = client.post(url_moves)
    assert response.status_code == 200
    player1_moves = response.json()
    assert len(player1_moves["moves"]) == 3  #Verifica que se reparten movimientos al jugador 1.
    
    #Se le reparten movimientos correctamente al usuario 2.
    url_moves = "http://localhost:8000/get_moves/1/2"
    response = client.post(url_moves)
    assert response.status_code == 200
    player2_moves = response.json()
    assert len(player2_moves["moves"]) == 3  #Verifica que se reparten movimientos al jugador 2.

def test_get_figures(client):
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
    client.post(url_join,json=payload)

    #Se inicia la partida.
    url_start = "http://localhost:8000/start_game/1"
    client.post(url_start)

    #Se obtienen las cartas reveladas del jugador 1.
    url_moves = "http://localhost:8000/get_figures/1/1"
    response = client.post(url_moves)
    assert response.status_code == 412

def test_use_moves_success(client,test_db,monkeypatch):

    def mock_shuffle(x):
        print("Funcion mockeada.")
        x.sort()
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

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

    #Pruebas de usar movimientos.
    users = uid_by_turns(1,test_db)
    url = "http://localhost:8000/use_moves"

    #Jugar movimiento correctamente
    payload = {
        'id_game': 1,
        'id_player': users[0],
        'name': 'mov1',
        'pos1': [0,0],
        'pos2': [2,2]
    }
    response = client.post(url, json=payload)
    assert response.status_code == 200

def test_use_moves_invalid_turn(client,test_db,monkeypatch):

    def mock_shuffle(x):
        print("Funcion mockeada.")
        x.sort()
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

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

    #Pruebas de usar movimientos.
    users = uid_by_turns(1,test_db)
    url = "http://localhost:8000/use_moves"

    #Intentar jugar movimiento si no es su turno.
    payload = {
        'id_game': 1,
        'id_player': users[1],
        'name': 'mov1',
        'pos1': [0,0],
        'pos2': [2,2]
    }
    response = client.post(url, json=payload)
    assert response.status_code == 412

def test_use_moves_invalid_move(client,test_db,monkeypatch):

    def mock_shuffle(x):
        print("Funcion mockeada.")
        x.sort()
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

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

    #Pruebas de usar movimientos.
    users = uid_by_turns(1,test_db)
    url = "http://localhost:8000/use_moves"

    #Intentar jugar un movimiento que el usuario no tiene.
    payload = {
        'id_game': 1,
        'id_player': users[0],
        'name': 'mov4',
        'pos1': [0,0],
        'pos2': [1,1]
    }
    response = client.post(url, json=payload)
    assert response.status_code == 404

def test_use_moves_invalid_position(client,test_db,monkeypatch):

    def mock_shuffle(x):
        print("Funcion mockeada.")
        x.sort()
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

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

    #Pruebas de usar movimientos.
    users = uid_by_turns(1,test_db)
    url = "http://localhost:8000/use_moves"

    #Intentar jugar un movimiento con posiciones invalidas.
    payload = {
        'id_game': 1,
        'id_player': users[0],
        'name': 'mov1',
        'pos1': [0,0],
        'pos2': [2,3]
    }
    response = client.post(url, json=payload)
    assert response.status_code == 409

#def test_use_figures(client):