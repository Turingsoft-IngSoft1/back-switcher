from pydantic import BaseModel, Field
from models.move import valid_moves


def generate_moves(name: str, initial_position: tuple[int, int]) -> list[tuple[int, int]]:
    """Genera movimientos disponibles en función del nombre y la posición inicial."""\
    """Sanitiza movimientos fuera de límites establecidos por el tablero."""
    available_moves = []
    match name:
        case "mov1":
            available_moves.extend([
                (initial_position[0] + 2, initial_position[1] - 2),
                (initial_position[0] - 2, initial_position[1] - 2),
                (initial_position[0] + 2, initial_position[1] + 2),
                (initial_position[0] - 2, initial_position[1] + 2)
            ])
        case "mov2":
            available_moves.extend([
                (initial_position[0], initial_position[1] + 2),
                (initial_position[0], initial_position[1] - 2),
                (initial_position[0] + 2, initial_position[1]),
                (initial_position[0] - 2, initial_position[1])
            ])
        case "mov3":
            available_moves.extend([
                (initial_position[0], initial_position[1] + 1),
                (initial_position[0], initial_position[1] - 1),
                (initial_position[0] + 1, initial_position[1]),
                (initial_position[0] - 1, initial_position[1])
            ])
        case "mov4":
            available_moves.extend([
                (initial_position[0] + 1, initial_position[1] + 1),
                (initial_position[0] + 1, initial_position[1] - 1),
                (initial_position[0] - 1, initial_position[1] + 1),
                (initial_position[0] - 1, initial_position[1] - 1)
            ])
        case "mov5":
            available_moves.extend([
                (initial_position[0] + 1, initial_position[1] - 2),
                (initial_position[0] + 2, initial_position[1] + 1),
                (initial_position[0] - 1, initial_position[1] + 2),
                (initial_position[0] - 2, initial_position[1] - 1)
            ])
        case "mov6":
            available_moves.extend([
                (initial_position[0] + 2, initial_position[1] - 1),
                (initial_position[0] + 1, initial_position[1] - 2),
                (initial_position[0] - 2, initial_position[1] - 1),
                (initial_position[0] - 1, initial_position[1] - 2)
            ])
        case "mov7":
            available_moves.extend([
                (initial_position[0], 5),
                (initial_position[0], 0),
                (5, initial_position[1]),
                (0, initial_position[1])
            ])

    valid_moves_in_bounds = [
        (x, y) for x, y in available_moves if 0 <= x < 6 and 0 <= y < 6
    ]
    
    return valid_moves_in_bounds


class Move(BaseModel):
    """Schema for move cards implementation"""
    name: str = Field(min_length=4, max_length=4, description="Name of the move.")
    initial_position: tuple[int, int] = Field(description="Initial position of the move.")
    available_moves: list[tuple[int, int]] = Field(default_factory=list, description="List of possible moves.")

    def __init__(self, **data):
        super().__init__(**data)
        if self.name not in valid_moves:
            raise ValueError("Invalid move name")
        if not (0 <= self.initial_position[0] < 6 and 0 <= self.initial_position[1] < 6):
            raise ValueError("Invalid initial position")
        self.available_moves = generate_moves(self.name, self.initial_position)
