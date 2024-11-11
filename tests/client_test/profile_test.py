import json

def test_new_profile(client):
    #Crear PartidaEjemplo y UsuarioEjemplo. 
    url = "http://localhost:8000/create_game"
    payload = {
        "game_name": "PartidaEjemplo",
        "owner_name": "UsuarioEjemplo",
        "min_player": 2,
        "max_player": 2
    }