from sqlalchemy.exc import SQLAlchemyError
from random import shuffle
from models.user import UserTable
from schemas.response_models import CurrentUsers
from schemas.user_schema import User
from models import GameTable

def create_user(name: str, id_game: int, db):
    """Crear un usuario y agregarlo."""
    try:
        new_user = UserTable(name=name, id_game=id_game)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User {new_user.name} created")
        return new_user.id
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error: {e}")
    

def remove_user(id_user: int, db):
    """Elimina de la base de datos al jugador con el id correspondiente."""
    to_remove = db.query(UserTable).filter(UserTable.id == id_user).first()
    try:
        db.delete(to_remove)
        db.commit()
        print(f"User deleted.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error: {e}")
    


def get_users(id_game: int, db) :
    """Lista los jugadores activos en una partida."""
    users = db.query(UserTable).filter(UserTable.id_game == id_game).all()
    l = []
    for u in users:
        l.append(User(id=u.id,
                      name=u.name,
                      id_game=u.id_game,
                      turn=u.turn))
    return l

def set_users_turn(id_game: int, players: int, db) -> int :
    """Le asigna turnos al azar a los jugadores."""
    try:
        users = db.query(UserTable).filter(UserTable.id_game == id_game).all()
        shuffle(users)
        for index, user in enumerate(users, start=0):
            user.turn = index
        db.commit() 
        return users[0].id
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error: {e}")

def get_user_from_turn(id_game: int, turn: int, db) -> int:
    """Devuelve el ID del usuario correspondiente al turno especificado."""
    users = db.query(UserTable).filter(UserTable.id_game == id_game,
                                       UserTable.turn == turn).first()
    return users.id

def reorder_turns(id_game: int, db):
    """Actualiza el orden de los usuarios."""
    try:
        users = db.query(UserTable).filter(UserTable.id_game == id_game).order_by(UserTable.turn).all()
        # Actualizar los turnos en la base de datos
        for idx, usuario in enumerate(users, start=0):
            usuario.turn = idx
            db.add(usuario)
        db.commit()
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error: {e}")

def is_user_current_turn(id_game: int, id_user: int, db) -> bool:
    """Verifica si el usuario tiene el turno actual."""
    user = db.query(UserTable).filter(UserTable.id == id_user).first()
    game = db.query(GameTable).filter(GameTable.id == id_game).first()
    return (game.state == "Playing" and (user.turn == (game.turn % game.players)))

def uid_by_turns(id_game: int, db) -> list[int]:
    """Lista los jugadores segun su turno."""
    users = db.query(UserTable).filter(UserTable.id_game == id_game).order_by(UserTable.turn).all()
    return [u.id for u in users]

    