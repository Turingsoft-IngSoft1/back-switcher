import unittest
import requests
import json
from http.client import responses

from main import db

db.teardown()

class TestPregame(unittest.TestCase):

    def test_create_game(self):

        url = "http://localhost:8000/create_game"
        payload = {
            "game_name": "PartidaEjemplo",
            "owner_name": "UsuarioEjemplo",
            "min_player": 2,
            "max_player": 4
        }
        response = requests.post(url,json=payload)
        self.assertEqual(response.status_code,200)

        payload = {
                    "game_name": "PartidaErronea",
                    "owner_name": "UsuarioErroneo",
                    "min_player": 2,
                    "max_player": 1
                }
        response = requests.post(url,json=payload)
        self.assertEqual(response.status_code,422)
    
    def test_list_game(self):

        url = "http://localhost:8000/list_games"
        expected_json ={
        "games_list": [
            {
                "id": 1,
                "name": "PartidaEjemplo",
                "state": "Waiting",
                "turn": 0,
                "host": 1,
                "players": 1,
                "max_players": 4,
                "min_players": 2,
                "password": "password",
                "moves_deck": 50
            }
          ]
        }
        response = requests.get(url)
        formatted_response = json.dumps(response.json(), sort_keys=True)
        formatted_expected = json.dumps(expected_json, sort_keys=True)
        self.assertEqual(response.status_code,200)
        self.assertEqual(formatted_expected, formatted_response)

if __name__ == '__main__':
    unittest.main()