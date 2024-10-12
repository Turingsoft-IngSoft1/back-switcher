from random import shuffle,sample
from sqlalchemy.exc import SQLAlchemyError
from models.move import MoveTable
from querys.user_queries import uid_by_turns

moves = [f"mov{i}" for _ in range(7) for i in range(1, 8)]

def create_move(name: str, id_game: int, db):
    """Crear movimiento y agregarlo."""
    try:
        new_move = MoveTable(name=name, id_game=id_game)
        db.add(new_move)
        db.commit()
        db.refresh(new_move)
        return new_move.id
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def set_move_user(id: int, user_id: int, db):
    """Cambia el jugador al que pertenece el movimiento."""
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.user_id: user_id})
        db.commit()
        print("Set to new user")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def get_move_user(id: int, db) -> int:
    """Devuelve la id del jugador al cual le pertenece el movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.user_id

def get_move_name(id: int, db) -> str:
    """Devuelve el nombre del movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.name


def get_move_status(id: int, db) -> str:
    """Devuelve el status a la que pertenece el movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.status

def set_move_status(id: int, status: str, db):
    """Cambia el status a la que pertence el movimiento."""
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.status: status})
        db.commit()
        print(f"Set to different status.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def get_deck(id_game: int, db):
    """Devuelve el mazo de movimientos."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.status == "Deck").all()
    deck = []
    for i in ret:
        deck.append(i.id)
    return deck

def moves_in_deck(id_game: int, db) -> int:
    """Devuelve la cantidad de movimientos en el mazo."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.status == "Deck").count()
    return ret

def moves_in_hand(id_game: int, user_id: int, db) -> int:
    """Devuelve la cantidad de movimientos que el usuario tiene en mano."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.user_id == user_id,
                                     MoveTable.status == "InHand").count()
    return ret

def refill_moves(id_game: int, db):
    """Devuelve todos los movimientos descartados al mazo."""
    try:
        ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                         MoveTable.status == "Discarded").all()
        for m in ret:
            m.status = "Deck"
            db.add(m)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def remove_move(id: int, db):
    """Elimina de la base de datos el movimiento con el id correspondiente."""
    toRemove = db.query(MoveTable).filter(MoveTable.id == id).first()
    try:
        db.delete(toRemove)
        db.commit()
        print(f"Move deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

def refill_hand(id_game: int, user_id: int, n: int, db):
    """Se le rellena la mano con cartas de movimiento al jugador."""
    moves_on_deck = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                               MoveTable.status == "Deck").all()
    new_hand: list[str] = []
    for move in sample(moves_on_deck,n):
        move.user_id = user_id
        db.add(move)
        new_hand.append(move.name)
    db.commit()
    return new_hand

def get_hand(id_game: int, user_id: int, db):
    """Devuelve los nombres de los movimientos en mano."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                   MoveTable.user_id == user_id,
                                   MoveTable.status == "InHand").all()
    hand: list[str] = []
    for move in ret:
        hand.append(move.name)
    return hand

def initialize_moves(id_game: int, players: int, db):
    """"Crea todas las cartas de movimiento y se las reparte al azar a todos los jugadores."""
    shuffle(moves)
    users = uid_by_turns(id_game,db)
    try:
        for i in range(players):
            for j in range(3):
                m = MoveTable(name=moves[(3 * i) + j],
                            status="InHand",
                            user_id=users[i],
                            id_game=id_game)
                db.add(m)

        for j in range(3 * players, 49):
            m = MoveTable(name=moves[j],
                        id_game=id_game)
            db.add(m)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")
