from models import base
from models.user import UserTable

def create_user(name: str,game_id: int):
    """Crear un usuario y agregarlo."""
    db = base.SessionLocal()
    try:
        new_user = UserTable(name=name,game=game_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User {new_user.name} created")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
        return new_user.id

def get_games(id: int):
    """Devuelve el id del juego que el jugador esta jugando."""
    db = base.SessionLocal()
    ret = db.query(UserTable).filter(UserTable.id == id).first()
    return ret.game

def remove_user(id: int):
    """Elimina de la base de datos al jugador con el id correspondiente."""
    db = base.SessionLocal()
    toRemove = db.query(UserTable).filter(UserTable.id == id).first()
    try:
        db.delete(toRemove)
        db.commit()
        print(f"User deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
