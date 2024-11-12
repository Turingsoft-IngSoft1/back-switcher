from hashlib import blake2b
from random import randint
from typing import Dict

class ProfilesManager:
    def __init__(self):
        self.profiles: Dict[str, list[tuple[int, int]]] = {}

    def _hash_id(self, id: int) -> str:
        """Genera el hash para un ID."""
        return blake2b(str(id).encode()).hexdigest()

    def add_game(self, hashed_id: str, id_game: int, id_user: int):
        if hashed_id in self.profiles:
            self.profiles[hashed_id].append((id_game, id_user))

    def get_games(self, hashed_id: str) -> list[tuple[int, int]]:
        if hashed_id == "":
            return []
        return self.profiles.get(hashed_id, None)

    def remove_game(self, hashed_id: str, id_game: int, id_user: int):
        if hashed_id in self.profiles:
            try:
                self.profiles[hashed_id].remove((id_game, id_user))
            except ValueError:
                pass  # El juego no está en la lista, no hacer nada

    def get_new_profile(self) -> str:
        while True:
            random_id = randint(0, 8388607)
            hashed_id = self._hash_id(random_id)
            if hashed_id not in self.profiles:
                self.profiles[hashed_id] = []
                return hashed_id

PROFILES = ProfilesManager()
