from querys import board_queries
from schemas.response_models import ResponseCreate


def create(board_id: int):
    """Crear el tablero."""
    new_board_id = board_queries.create_board(board_id)
    return ResponseCreate(id_game=new_board_id)
