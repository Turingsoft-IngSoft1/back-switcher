from pydantic import BaseModel, Field


class Board(BaseModel):
    id: int = Field(description="Unique integer that specifies this board.")
    color: str = Field(min_length=1, max_length=10, description="Blocked color.", default=None)
    cells: list = Field(description="List of cells in the board.", default=[])
