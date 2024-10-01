import random

from models import base
from models.user import UserTable
from schemas.response_models import CurrentUsers
from schemas.user_schema import User


def create_user(name: str, game_id: int):
    """Crear un usuario y agregarlo."""
    db = base.SessionLocal()
    try:
        new_user = UserTable(name=name, game_id=game_id)
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


def get_game(user_id: int):
    """Devuelve el id del juego que el jugador esta jugando."""
    db = base.SessionLocal()
    ret = db.query(UserTable).filter(UserTable.id == user_id).first()
    ret = ret.game_id
    try:
        ret = ret.game_id.id
    finally:
        return ret


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


def get_users(game_id: int) -> CurrentUsers:
    """Lista los jugadores activos en una partida."""
    db = base.SessionLocal()
    try:
        users = db.query(UserTable).filter(UserTable.game_id == game_id).all()
        l = []
        for u in users:
            l.append(User(id=u.id,
                          name=u.name,
                          game=u.game_id,
                          figures_deck=u.figures_deck,
                          turn=u.turn))

        return CurrentUsers(users_list=l)
    except Exception as e:
        print(f"Error: {e}")
        return CurrentUsers(users_list=[])


def set_users_turn(game_id: int, players: int) -> int :
    """Le asigna turnos al azar a los jugadores."""
    db = base.SessionLocal()
    first = 0
    try:
        users = db.query(UserTable).filter(UserTable.game_id == game_id).all()
        ramdom_turns = random.sample(range(players), players)
        for u, t in zip(users, ramdom_turns):
            u.turn = t
            if t==0:
                first = u.id
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
        return first

def get_user_from_turn(game_id: int, turn: int) -> int | None:
    db = base.SessionLocal()
    try:
        users = db.query(UserTable).filter(UserTable.game_id == game_id).all()
        user_tuples = [(user.id, user.turn) for user in users]

        for user_id, user_turn in user_tuples:
            if turn == user_turn:
                return user_id

        return user_tuples[0][0] #

    finally:
        db.close()