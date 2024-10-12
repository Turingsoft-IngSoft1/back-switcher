from random import shuffle
from sqlalchemy.exc import SQLAlchemyError
from models.figure import FigureTable
from querys.user_queries import uid_by_turns


easy_figures = [f"fige{i:02d}" for _ in range(2) for i in range(1, 8)]
hard_figures = [f"fig{i:02d}" for _ in range(2) for i in range(1, 19)]
ranges_dict = {
    2: {
        'easy': {0: range(0, 7), 1: range(7, 14)},
        'hard': {0: range(0, 18), 1: range(18, 36)}
    },
    3: {
        'easy': {0: range(0, 4), 1: range(4, 9), 2: range(9, 14)},
        'hard': {0: range(0, 12), 1: range(12, 24), 2: range(24, 36)}
    },
    4: {
        'easy': {0: range(0, 3), 1: range(3, 7), 2: range(7, 11), 3: range(11, 14)},
        'hard': {0: range(0, 9), 1: range(9, 18), 2: range(18, 27), 3: range(27, 36)}
    }
}

def create_figure(name: str, user_id: int, db):
    """Crear figura y agregarla."""
    try:
        new_figure = FigureTable(name=name, user_id=user_id)
        db.add(new_figure)
        db.commit()
        db.refresh(new_figure)
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
        
def initialize_figures(id_game: int, players: int, db):
    """"Crea todas las cartas de figura y se las reparte al azar a todos los jugadores."""
    shuffle(easy_figures)
    shuffle(hard_figures)

    users = uid_by_turns(id_game, db)

    try:
        for i in range(players):
            easy_range = ranges_dict[players]['easy'][i]
            hard_range = ranges_dict[players]['hard'][i]
            
            for j in easy_range:
                fig = FigureTable(name=easy_figures[j], id_game=id_game, user_id=users[i])
                db.add(fig)
            
            for k in hard_range:
                fig = FigureTable(name=hard_figures[k], id_game=id_game, user_id=users[i])
                db.add(fig)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")