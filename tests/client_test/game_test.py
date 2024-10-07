"""import json
import pytest
import requests
import unittest

from main import db


class TestGame(unittest.TestCase):
    @pytest.mark.order(0)
    def test_leave(self):
        db.teardown()
        url_create = "http://localhost:8000/create_game"
        payload = {
            "game_name": "PartidaEjemplo",
            "owner_name": "UsuarioEjemplo",
            "min_player": 2,
            "max_player": 4
        }
        requests.post(url_create, json=payload)

        urljoin = "http://localhost:8000/join_game"
        payload = {
            "id_game": 1,
            "player_name": "UsuarioParaLlenarLobby"
        }
        requests.post(urljoin, json=payload)

        url = "http://localhost:8000/leave_game"
        payload = {
            "id_player": 1,
            "id_game": 1
        }
        response = requests.post(url, json=payload)

        expected_json = {
            "message": "Exit Successful."
        }

        self.assertEqual(response.status_code, 200)
        formatted_response = json.dumps(response.json(), sort_keys=True)
        formatted_expected = json.dumps(expected_json, sort_keys=True)
        self.assertEqual(formatted_response, formatted_expected)

    @pytest.mark.order(1)
    def test_skip_turn(self):
        url = "http://localhost:8000/skip_turn"
        payload = {
          "id_player": 2,
          "id_game": 1
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
"""