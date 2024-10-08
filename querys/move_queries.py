from models.move import MoveTable


def create_move(name: str, id_game: int, db):
    """Crear movimiento y agregarlo."""
    try:
        new_move = MoveTable(name=name, id_game=id_game)
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


def get_move_user(id: int, db):
    """Devuelve la id del jugador al cual le pertenece el movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.user_id


def set_move_user(id: int, user_id: int, db):
    """Cambia el jugador al que pertenece el movimiento."""
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.user_id: user_id})
        db.commit()
        print("Set to new user")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


def get_move_name(id: int, db):
    """Devuelve el nombre del movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.name


def get_move_status(id: int, db):
    """Devuelve el status a la que pertenece el movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.status

def get_deck(id_game: int, db):
    """Devuelve el mazo de movimientos."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.status == "Deck").all()
    deck = []
    for i in range(len(ret)):
        deck.append(ret[i].id)
    return deck

def moves_in_deck(id_game: int, db):
    """Devuelve la cantidad de movimientos en el mazo."""
    ret = db.query(MoveTable).filter(MoveTable.id_game == id_game,
                                     MoveTable.status == "Deck").count()
    return ret

def moves_in_hand(id_game: int, user_id: int, db):
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
    finally:
        db.close()

def set_move_status(id: int, status: str, db):
    """Cambia el status a la que pertence el movimiento."""
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.status: status})
        db.commit()
        print(f"Set to different status.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

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
    finally:
        db.close()
