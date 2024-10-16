from typing import Dict
from schemas.board_schema import Board

class BoardsManager:
    """Clase manejadora de los tableros parciales."""

    def __init__(self):
        self._active_boards: Dict[int, Board] = {}

    def initialize(self, id_game: int, db):
        if id_game not in self._active_boards:
            self._active_boards[id_game] = Board.create(id_game,db)

    def update(self, id_game: int, p1: tuple[int,int], p2: tuple[int,int]):
        if id_game in self._active_boards:
            self._active_boards[id_game].aplly_move(p1,p2)
    
    def remove(self, id_game: int):
        if id_game in self._active_boards:
            del self._active_boards[id_game]
    
    def get(self, id_game: int) -> list[list[str]]:
        if id_game in self._active_boards:
            return self._active_boards.get(id_game).matrix

PARTIAL_BOARDS = BoardsManager()