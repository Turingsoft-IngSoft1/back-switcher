from models.figure import FigureTable
from querys.game_queries import get_players
import random


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
        
def initialize_figures(id_game: int, db):
    
    easy_figures = []
    hard_figures = []
    
    for _ in range(2):
        for i in range(1, 8):
                easy_figures.append((f"fige{i:02d}"))     
        for i in range(1,19):     
                hard_figures.append((f"fig{i:02d}"))
    
    random.shuffle(easy_figures)
    random.shuffle(hard_figures)
    
    player_count = get_players(id_game, db)
    
    for player in range(player_count):
        
        for _ in range(round(14/player_count)):
            random_easy_figure = easy_figures.pop()
            create_figure(random_easy_figure, player, db)
            
        for _ in range(round(36/player_count)):
            random_hard_figure = hard_figures.pop()
            create_figure(random_hard_figure, player, db)
