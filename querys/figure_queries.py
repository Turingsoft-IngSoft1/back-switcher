from models.figure import FigureTable
from querys.user_queries import uid_by_turns
from random import sample

easy_figures = [f"fige{i:02d}" for _ in range(2) for i in range(1, 8)]
hard_figures = [f"fig{i:02d}" for _ in range(2) for i in range(1, 19)]
    

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
    parts1 = [(14//players) + 1 if i < (14%players) else (14//players) for i in range(players)]
    parts2 = [(36//players) + 1 if i < (36%players) else (36//players) for i in range(players)]
    
    for p1,p2,u in zip(parts1,parts2,uid_by_turns(id_game,db)):
        ef = sample(easy_figures,p1)
        hf = sample(hard_figures,p2)
        for name in ef:
            create_figure(name,u,db)
        for name in hf:
            create_figure(name,u,db)
