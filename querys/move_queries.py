from random import shuffle,sample
from sqlalchemy.exc import SQLAlchemyError
from models.move import MoveTable
from querys.user_queries import uid_by_turns

moves = [f"mov{i}" for _ in range(7) for i in range(1, 8)]

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
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")

def refill_hand(id_game: int, user_id: int, n: int, db):
    """Se le rellena la mano con cartas de movimiento al jugador."""
    moves_on_deck = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                               MoveTable.status == "Deck").all()
    new_hand: list[str] = []
    for move in sample(moves_on_deck,n):
        move.user_id = user_id
        move.status = "InHand"
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

