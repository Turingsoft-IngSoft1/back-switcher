from pydantic import BaseModel, Field
from querys.board_queries import get_board,get_color

class Board(BaseModel):
    id_game: int = Field(description="Unique integer that specifies this board.")
    color: str = Field(min_length=1, max_length=10, description="Blocked color.")
    matrix: list[list[str]] = Field(description="List of cells in the board.")

    @classmethod
    def create(cls, id_game: int):
        color = get_color(id_game)
        matrix = get_board(id_game)
        return cls(id_game=id_game, color=color, matrix=matrix)