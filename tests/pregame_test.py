import unittest
import requests

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

if __name__ == '__main__':
    unittest.main()