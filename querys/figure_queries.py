from models.figure import FigureTable


def create_figure(name: str, user_id: int, db):
    """Crear figura y agregarla."""
    try:
        new_figure = FigureTable(name=name, user_id=user_id)
        db.add(new_figure)
        db.commit()
        db.refresh(new_figure)
        print(f"Figure {new_figure.name} created")
        return new_figure.id
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


def get_figure_user(id: int, db):
    """Devuelve la id del jugador al cual le pertenece la figura."""
    ret = db.query(FigureTable).filter(FigureTable.id == id).first()
    return ret.user_id


def get_figure_name(id: int, db):
    """Devuelve el nombre de la figura."""
    ret = db.query(FigureTable).filter(FigureTable.id == id).first()
    return ret.name


def remove_figure(id: int, db):
    """Elimina de la base de datos la figura con el id correspondiente."""
    toRemove = db.query(FigureTable).filter(FigureTable.id == id).first()
    try:
        db.delete(toRemove)
        db.commit()
        print(f"Figure deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
