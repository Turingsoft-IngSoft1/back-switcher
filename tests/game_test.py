import requests
import json
import unittest

from main import db


db.teardown()

class TestGame(unittest.TestCase):
    def test6_leave(self):
        url_create = "http://localhost:8000/create_game"
        payload = {
            "game_name": "PartidaEjemplo",
            "owner_name": "UsuarioEjemplo",
            "min_player": 2,
            "max_player": 4
        }
        requests.post(url_create,json=payload)
        
        urljoin = "http://localhost:8000/join_game"
        payload = {
            "id_game": 1,
            "player_name": "UsuarioParaLlenarLobby"
        }
        requests.post(urljoin,json=payload)
        
        url = "http://localhost:8000/leave_game"
        payload = {
            "id_player": 1,
            "id_game": 1
        }
        response = requests.post(url,json=payload)
        
        expected_json = {
            "message": "Exit Successful."
        }
        
        self.assertEqual(response.status_code, 200)
        formatted_response = json.dumps(response.json(), sort_keys=True)
        formatted_expected = json.dumps(expected_json, sort_keys=True)
        self.assertEqual(formatted_response, formatted_expected)
        
                   
if __name__ == '__main__':
    unittest.main()

