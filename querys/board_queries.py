from models import base
from models.board import BoardTable
from schemas import board_schema


def create_board(board_id:int): #Chequear si va id
    """Crea un tablero y lo inserta en la base de datos."""
    db = base.SessionLocal()
    try:
        new_board = BoardTable(id=board_id)
        db.add(new_board)
        db.commit()
        db.refresh(new_board)
        print(f"Board {new_board.id} created")
    except Exception as e:
        db.rollback()
        print(f"Error creating board: {e}")
    finally:
        db.close()
        return new_board.id
    

def get_board(board_id: int) -> board_schema.Board:
    """Encuentra y muestra el tablero que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    board_Ret = db.query(BoardTable).filter(BoardTable.id == board_id).first()
    return board_schema.Board(id=board_Ret.id,
                            color=board_Ret.color,
                            cells=board_Ret.cells)

def get_color(board_id: int) -> str:
    """Encuentra y muestra el color bloqueado del tablero que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    color_Ret = db.query(BoardTable).filter(BoardTable.id == board_id).first()
    return color_Ret.color

def modify_cell(board_id: int, cell: int, color: str):
    """Modifica una celda en específico del tablero."""
    db = base.SessionLocal()
    db.query(BoardTable).filter(BoardTable.id == board_id).update({BoardTable.cells[cell]: color})
    db.commit()
    db.close()
    