import random
from models.user import UserTable
from schemas.response_models import CurrentUsers
from schemas.user_schema import User


def create_user(name: str, id_game: int, db):
    """Crear un usuario y agregarlo."""
    try:
        new_user = UserTable(name=name, id_game=id_game)
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


def get_game(user_id: int, db):
    """Devuelve el id del juego que el jugador esta jugando."""
    ret = db.query(UserTable).filter(UserTable.id == user_id).first()
    ret = ret.id_game
    try:
        ret = ret.id_game.id
    finally:
        return ret


def remove_user(user_id: int, db):
    """Elimina de la base de datos al jugador con el id correspondiente."""
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


def get_users(id_game: int, db) -> CurrentUsers:
    """Lista los jugadores activos en una partida."""
    try:
        users = db.query(UserTable).filter(UserTable.id_game == id_game).all()
        l = []
        for u in users:
            l.append(User(id=u.id,
                          name=u.name,
                          game=u.id_game,
                          figures_deck=u.figures_deck,
                          turn=u.turn))

        return CurrentUsers(users_list=l)
    except Exception as e:
        print(f"Error: {e}")
        return CurrentUsers(users_list=[])


def set_users_turn(id_game: int, players: int, db) -> int :
    """Le asigna turnos al azar a los jugadores."""
    first = 0
    try:
        users = db.query(UserTable).filter(UserTable.id_game == id_game).all()
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

def get_user_from_turn(id_game: int, turn: int, db) -> int | None:
    try:
        users = db.query(UserTable).filter(UserTable.id_game == id_game).all()
        user_tuples = [(user.id, user.turn) for user in users]

        for user_id, user_turn in user_tuples:
            if turn == user_turn:
                return user_id

        return user_tuples[0][0] #

    finally:
        db.close()