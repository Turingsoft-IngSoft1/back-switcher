from models.move import MoveTable


def create_move(name: str, id_game, db):
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


def get_users(id: int, db):
    """Devuelve la id del jugador al cual le pertenece el movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.user_id


def set_users(id: int, user_id: int, db):
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


def get_move_pile(id: int, db):
    """Devuelve la pila a la que pertenece el movimiento."""
    ret = db.query(MoveTable).filter(MoveTable.id == id).first()
    return ret.pile


def set_move_pile(id: int, pile: str, db):
    """Cambia la pila a la que pertence el movimiento."""
    try:
        db.query(MoveTable).filter(MoveTable.id == id).update({MoveTable.pile: pile})
        db.commit()
        print(f"Set to different pile.")
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
