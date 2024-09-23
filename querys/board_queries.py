from models import base
from models.board import BoardTable
from schemas import board_schema

def create_board(id:int, color:str): #Chequear si va id
    """Crea un tablero y lo inserta en la base de datos."""
    db = base.SessionLocal()
    try:
        new_board = BoardTable(id=id,
                               color=color)
        db.add(new_board)
        db.commit()
        db.refresh(new_board)
        print(f"Board {new_board.id} created")
    except Exception as e:
        db.rollback()
        print(f"Error creating board: {e}")
    finally:
        db.close()
        #return?
    

def get_board(id: int) -> board_schema.Board:
    """Encuentra y muestra el tablero que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    board_Ret = db.query(BoardTable).filter(BoardTable.id == id).first()
    return board_schema.Board(id=board_Ret.id,
                            color=board_Ret.color)

def get_color(id: int) -> str:
    """Encuentra y muestra el color bloqueado del tablero que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    color_Ret = db.query(BoardTable).filter(BoardTable.id == id).first()
    return color_Ret.color
