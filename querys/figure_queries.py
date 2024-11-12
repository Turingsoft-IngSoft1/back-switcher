from random import shuffle,sample
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
                fig = FigureTable(name=easy_figures[j],
                                  id_game=id_game,
                                  id_user=users[i])
                db.add(fig)
            
            for k in hard_range:
                fig = FigureTable(name=hard_figures[k],
                                  id_game=id_game,
                                  id_user=users[i])
                db.add(fig)

        db.commit()
        
        for u in users:
            figures = db.query(FigureTable).filter_by(id_game=id_game, id_user=u,status="Hidden").all()
            sampled_figures = sample(figures, 3)
            for fig in sampled_figures:
                fig.status = "Revealed"
        
        db.commit()
            
    except SQLAlchemyError as e:  #pragma: no cover
        db.rollback()  #pragma: no cover
        print(f"Error de SQLAlchemy: {str(e)}")  #pragma: no cover

def get_revealed_figures(id_game: int, db):
    """Devuelve una lista con las figuras reveladas de un juego."""
    figures = db.query(FigureTable).filter_by(id_game=id_game, status="Revealed").all()
    revealed_figures = {u: [] for u in uid_by_turns(id_game, db)}
    for fig in figures:
        if fig.id_user in revealed_figures:
            revealed_figures[fig.id_user].append(fig.name)

    return revealed_figures

def get_blocked_figures(id_game: int, db):
    """Devuelve una lista con las figuras bloqueadas de un juego."""
    figures = db.query(FigureTable).filter_by(id_game=id_game, status="Blocked").all()
    blocked_figures = {u: [] for u in uid_by_turns(id_game, db)}
    for fig in figures:
        if fig.id_user in blocked_figures:
            blocked_figures[fig.id_user].append(fig.name)

    return blocked_figures


def refill_revealed_figures(id_game: int, id_user: int, db):
    """Revela las figuras faltantes del jugador."""
    try:
        c = db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Revealed").count()
        hidden = db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Hidden").all()
        sampled_figures = sample(hidden, 3-c)
        for fig in sampled_figures:
            fig.status = "Revealed"
        db.commit()
    except SQLAlchemyError as e:  #pragma: no cover
        db.rollback()  #pragma: no cover
        print(f"Error de SQLAlchemy: {str(e)}")  #pragma: no cover

def figures_in_hand(id_game: int, id_user: int, db):
    """Devuelve la cantidad de figuras en la mano del jugador."""
    return db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Revealed").count()

def use_figure(id_game: int, id_user: int, figure_name: str, db):
    """Usa una figura."""
    try:
        figure = db.query(FigureTable).filter(FigureTable.id_game == id_game,
                                              FigureTable.id_user == id_user,
                                              FigureTable.name == figure_name,
                                              FigureTable.status == "Revealed").first()
        figure.status = "Discarded"
        db.commit()
    except SQLAlchemyError as e:  #pragma: no cover
        db.rollback()  #pragma: no cover
        print(f"Error de SQLAlchemy: {str(e)}")  #pragma: no cover

def block_figure(id_game: int, id_user: int, figure_name: str, db):
    """Usa una figura."""
    try:
        figure = db.query(FigureTable).filter(FigureTable.id_game == id_game,
                                              FigureTable.id_user == id_user,
                                              FigureTable.name == figure_name,
                                              FigureTable.status == "Revealed").first()
        figure.status = "Blocked"
        db.commit()
    except SQLAlchemyError as e:  #pragma: no cover
        db.rollback()  #pragma: no cover
        print(f"Error de SQLAlchemy: {str(e)}")  #pragma: no cover
        
def figures_in_deck(id_game: int, id_user: int, db):
    """Devuelve la cantidad de figuras en el mazo del jugador."""
    return db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Hidden").count()

def is_user_blocked(id_game: int, id_user: int, db):
    return (db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Blocked").count() == 1)

def unblock_figure(id_game: int, id_user: int, db):
    """Desbloquea la figura bloqueada si puede hacerlo."""
    if ((db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Blocked").count() == 1) and
        (db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Revealed").count() == 0)):
        
        try:
            f = db.query(FigureTable).filter_by(id_game=id_game, id_user=id_user, status="Blocked").first()
            f.status = "Revealed"
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()  #pragma: no cover
            print(f"Error de SQLAlchemy: {str(e)}")  #pragma: no cover