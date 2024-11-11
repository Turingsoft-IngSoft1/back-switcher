import json

def test_profile(client):
    #Crear PartidaEjemplo y UsuarioEjemplo. 
    url_profile = "http://localhost:8000/new_profile"
    response = client.get(url_profile)
    user_profile = response.text

    assert user_profile is not None

    url_create = f"http://localhost:8000/create_game?profile_id={user_profile}"
    payload = {
        "game_name": "Partida",
        "owner_name": "Usuario1",
        "min_player": 2,
        "max_player": 2,
        "password": ""
    }
    client.post(url_create, json=payload)

    url = "http://localhost:8000/join_game"
    payload = {
        "id_game": 1,
        "player_name": "Usuario2",
        "password": ""
    }
    client.post(url_create, json=payload)

    url = "http://localhost:8000/start_game/1"
    client.post(url)

    url_load = f"http://localhost:8000/load_profile/{user_profile}"
    user_games = client.get(url_load)
    assert user_games[0].id_game == 1