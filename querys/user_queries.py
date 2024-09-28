from models import base
from models.user import UserTable
from schemas.response_models import CurrentUsers
from schemas.user_schema import User

def create_user(name: str,game_id: int):
    """Crear un usuario y agregarlo."""
    db = base.SessionLocal()
    try:
        new_user = UserTable(name=name,game_id=game_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User {new_user.name} created")
        return new_user.id
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

def get_game(user_id: int) :
    """Devuelve el id del juego que el jugador esta jugando."""
    db = base.SessionLocal()
    ret = db.query(UserTable).filter(UserTable.id == user_id).first()
    return ret.game_id

def remove_user(user_id: int):
    """Elimina de la base de datos al jugador con el id correspondiente."""
    db = base.SessionLocal()
    to_remove = db.query(UserTable).filter(UserTable.id == user_id).first()
    try:
        db.delete(to_remove)
        db.commit()
        print(f"User deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

def get_users(user_id: int) -> CurrentUsers :
    """Lista los jugadores activos en una partida."""
    db = base.SessionLocal()
    try:
        users = db.query(UserTable).filter(UserTable.id == user_id).all()
        l = []
        for u in users:
            l.append(User(id=u.id,
                          name=u.name,
                          game=u.game_id,
                          figures_deck=0))
    
        return CurrentUsers(users_list=l)
    except Exception:
        return CurrentUsers(users_list=[])
    