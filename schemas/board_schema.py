from pydantic import BaseModel, Field
from querys.board_queries import get_board,get_color

class Board(BaseModel):
    id_game: int = Field(description="Unique integer that specifies this board.")
    color: str = Field(min_length=1, max_length=10, description="Blocked color.")
    board_cells: list[list[str]] = Field(description="List of cells in the board.")

    def __init__(self, id_game: int):
        super().__init__(id_game=id_game)
        self.color = get_color(id_game)
        self.board_cells = get_board(id_game)