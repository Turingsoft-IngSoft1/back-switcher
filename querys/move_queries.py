from random import shuffle,sample
from sqlalchemy.exc import SQLAlchemyError
from models.move import MoveTable
from querys.user_queries import uid_by_turns

moves = [f"mov{i}" for _ in range(7) for i in range(1, 8)]

def initialize_moves(id_game: int, players: int, db):
    """Crea todas las cartas de movimiento y se las reparte al azar a todos los jugadores."""
    shuffle(moves)
    users = uid_by_turns(id_game,db)
    try:
        for i in range(players):
            for j in range(3):
                m = MoveTable(name=moves[(3 * i) + j],
                              status="InHand",
                              id_user=users[i],
                              id_game=id_game)
                db.add(m)

        for k in range(3 * players, 49):
            m = MoveTable(name=moves[k],
                          id_game=id_game)
            db.add(m)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")

def moves_in_deck(id_game: int, db) -> int:
    """Devuelve la cantidad de movimientos en el mazo."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.status == "Deck").count()
    return ret

def moves_in_hand(id_game: int, id_user: int, db) -> int:
    """Devuelve la cantidad de movimientos que el usuario tiene en mano."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.id_user == id_user,
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
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")

def refill_hand(id_game: int, id_user: int, need: int, db):
    """Rellena la mano del jugador con la cantidad de movimientos necesarios."""
    try:
        moves_on_deck = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                                   MoveTable.status == "Deck").all()
        new_hand = []
        for move in sample(moves_on_deck, need):
            move.id_user = id_user
            move.status = "InHand"
            db.add(move)
            new_hand.append(move.name)
        db.commit()
        return new_hand
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")

def get_hand(id_game: int, id_user: int, db):
    """Devuelve los nombres de los movimientos en la mano del jugador."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.id_user == id_user,
                                     MoveTable.status == "InHand").all()
    hand = []
    for move in ret:
        hand.append(move.name)
    return hand

