import json,pytest
from unittest.mock import patch

@pytest.mark.order(0)
def test_leave(mocker,test_db,client):
    mocker.patch("utils.database.SERVER_DB", test_db)

    url_create = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 4
    }
    client.post(url_create, json=payload)

    urljoin = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "UsuarioParaLlenarLobby"
    }
    client.post(urljoin, json=payload)

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

@pytest.mark.order(1)
def test_skip_turn(mocker,test_db,client):
    mocker.patch("utils.database.SERVER_DB", test_db)

    url = "http://localhost:8000/skip_turn"
    payload = {
      "id_player": 2,
      "id_game": 1
    }
    response = client.post(url, json=payload)
    assert response.status_code == 200