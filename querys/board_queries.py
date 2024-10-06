from models import base
from models.board import BoardTable,BoardValidationError

def create_board(id_game: int):  # Chequear si va id
    """Crea un tablero y lo inserta en la base de datos."""
    db = base.SessionLocal()
    try:
        new_board = BoardTable(id_game=id_game)
        db.add(new_board)
        db.commit()
        db.refresh(new_board)
        print(f"Board {new_board.id} created")
        return new_board.id
    except Exception as e:
        db.rollback()
        print(f"Error creating board: {e}")
    finally:
        db.close()

def get_board(id_game: int) :
    """Encuentra y muestra el tablero que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    board_ret = db.query(BoardTable).filter(BoardTable.id_game == id_game).first()
    return board_ret.get_board()

def get_color(id_game: int) -> str:
    """Encuentra y muestra el color bloqueado del tablero que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    color_ret = db.query(BoardTable).filter(BoardTable.id_game == id_game).first()
    return color_ret.color

def update_board(id_game: int, matrix: list[list[str]]):
    db = base.SessionLocal()
    try:
        b_table = db.query(BoardTable).filter(BoardTable.id_game == id_game).first()
        b_table.board_json = matrix
        db.commit()
        print(f"Board {b_table.id} updated")
    except BoardValidationError as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()