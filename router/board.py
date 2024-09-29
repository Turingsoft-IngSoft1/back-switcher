from fastapi import APIRouter,HTTPException
from schemas.game_schema import Game
from schemas.board_schema import Board
from querys import board_queries
from schemas.response_models import ResponseCreate,ResponseJoin,ResponseList

def create(board_id: int):
    """Crear el tablero."""
    new_board_id = board_queries.create_board(board_id)
    return ResponseCreate(id_game=new_board_id)

