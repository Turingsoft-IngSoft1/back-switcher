from models import base
from models.move import MoveTable

def create_move(name: str):
    """Crear movimiento y agregarlo."""
    db = base.SessionLocal()
    try:
        new_move = MoveTable(name=name)
        db.add(new_move)
        db.commit()
        db.refresh(new_move)
        print(f"Move {new_move.name} created")
        return new_move.id
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
        
def get_users(id: int):
    """Devuelve la id del jugador al cual le pertenece el movimiento."""
    db = base.SessionLocal()
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.user_id

def set_users(id: int, user_id: int):
    """Cambia el jugador al que pertenece el movimiento."""
    db = base.SessionLocal()
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.user_id: user_id})
        db.commit()
        print("Set to new user")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

def get_move_name(id: int):
    """Devuelve el nombre del movimiento."""
    db = base.SessionLocal()
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.name

def get_move_pile(id: int):
    """Devuelve la pila a la que pertenece el movimiento."""
    db = base.SessionLocal()
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.pile

def set_move_pile(id: int, pile: str):
    """Cambia la pila a la que pertence el movimiento."""
    db = base.SessionLocal()
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.pile: pile})
        db.commit()
        print(f"Set to different pile.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

def remove_move(id: int):
    """Elimina de la base de datos el movimiento con el id correspondiente."""
    db = base.SessionLocal()
    toRemove = db.query(MoveTable).filter(MoveTable.id == id).first()
    try:
        db.delete(toRemove)
        db.commit()
        print(f"Move deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()