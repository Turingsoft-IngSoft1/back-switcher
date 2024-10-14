from pydantic import BaseModel, Field
from querys.board_queries import get_board,get_color

class Board(BaseModel):
    id_game: int = Field(description="Unique integer that specifies this board.")
    color: str = Field(min_length=1, max_length=3, description="Blocked color.")
    matrix: list[list[str]] = Field(description="List of cells in the board.")

    def aplly_move(self, p1:tuple[int,int], p2:tuple[int,int]):
        self.matrix[p1[1]][p1[0]], self.matrix[p2[1]][p2[0]] = (
            self.matrix[p2[1]][p2[0]],
            self.matrix[p1[1]][p1[0]],
        )

    @classmethod
    def create(cls, id_game: int, db):
        color = get_color(id_game, db)
        matrix = get_board(id_game, db)
        if (matrix is None) or (color is None):
            raise ValueError("Invalid create.")
        return cls(id_game=id_game, color=color, matrix=matrix)
    