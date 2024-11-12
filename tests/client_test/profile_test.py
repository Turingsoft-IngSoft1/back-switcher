import json
from pytest import MonkeyPatch
from querys import uid_by_turns

def test_profile(client):
    #Crear PartidaEjemplo y UsuarioEjemplo. 
    url_profile = "http://localhost:8000/new_profile"
    response = client.get(url_profile)
    user_profile = response.text.strip("\"")

    assert user_profile is not None

    url_create = f"http://localhost:8000/create_game?profile_id={user_profile}"
    print(url_create)
    payload = {
        "game_name": "Partida",
        "owner_name": "Usuario1",
        "min_player": 2,
        "max_player": 2,
        "password": ""
    }
    client.post(url_create, json=payload)
    
    url_join = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "Usuario2",
        "password": ""
    }
    client.post(url_join, json=payload)

    url = "http://localhost:8000/start_game/1"
    client.post(url)

    url_load = f"http://localhost:8000/load_profile/{user_profile}"
    response = client.get(url_load)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list) and len(data) > 0
    first_item = data[0]
    assert isinstance(first_item, dict)
    
    assert (first_item['id_game'] == 1 and
            first_item['game_name'] == 'Partida' and
            first_item['players'] == 2 and
            first_item['id_user'] == 1 and
            first_item['user_name'] == 'Usuario1')
    
def test_recover_game_data(client, monkeypatch, test_db):
    def mock_shuffle(x):
        x.sort()
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    def mock_get(self, game_id):
        board = [
        ["R", "R", "B", "Y", "G", "Y"], 
        ["R", "R", "Y", "B", "R", "R"], 
        ["B", "Y", "G", "G", "B", "Y"], 
        ["Y", "B", "G", "G", "Y", "B"], 
        ["R", "G", "B", "Y", "G", "B"], 
        ["G", "R", "Y", "B", "G", "R"]
        ]

        return board
    monkeypatch.setattr('utils.partial_boards.BoardsManager.get', mock_get)

    url_create = "http://localhost:8000/create_game"
    print(url_create)
    payload = {
        "game_name": "Partida",
        "owner_name": "Usuario1",
        "min_player": 2,
        "max_player": 2,
        "password": ""
    }
    client.post(url_create, json=payload)
    
    url_join = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "Usuario2",
        "password": ""
    }
    client.post(url_join, json=payload)

    # Usar antes de empezar la partida.
    url = "http://localhost:8000/recover_game_data/1/1/"
    response = client.get(url)
    assert response.status_code == 404

    url = "http://localhost:8000/start_game/1"
    client.post(url)

    # Usar en un user id erroneo.
    url = "http://localhost:8000/recover_game_data/1/40/"
    response = client.get(url)
    assert response.status_code == 404

    # Caso de exito.
    url = "http://localhost:8000/recover_game_data/1/1/"
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()

    expected_board = [
        ["R", "R", "B", "Y", "G", "Y"], 
        ["R", "R", "Y", "B", "R", "R"], 
        ["B", "Y", "G", "G", "B", "Y"], 
        ["Y", "B", "G", "G", "Y", "B"], 
        ["R", "G", "B", "Y", "G", "B"], 
        ["G", "R", "Y", "B", "G", "R"]
    ]

    assert data['actual_board'] == expected_board
    assert data['blocked_color'] == 'NOT'
    assert data['actual_turn_player'] == uid_by_turns(1,test_db)[0]
    assert data['available_moves'] == ['mov1', 'mov1', 'mov1']
    assert data['partial_moves'] == []