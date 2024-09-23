from typing import List
from models import base
from models.game import GameTable
from schemas.game_schema import Game

def create_game(name: str, host: str, max_players: int, min_players: int):
    """Crea una partida y la inserta en la base de datos."""
    db = base.SessionLocal()
    try:
        new_game = GameTable(name=name, host=host, max_players=max_players, min_players=min_players)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        print(f"Game {new_game.id} created")
        return new_game.id
    except Exception as e:
        db.rollback()
        print(f"Error creating game: {e}")
    finally:
        db.close()

def get_game(id_game: int) -> Game:
    """Encuentra y muestra el juego que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    g = db.query(GameTable).filter(GameTable.id == id_game).first()
    return Game(id=g.id, name=g.name,
                state=g.state, turn=g.turn,
                host=g.host, players=g.players,
                max_players=g.max_players, min_players=g.min_players,
                password=g.password)

def list_games() -> List[Game]:
    """Devuelve la lista de las partidas en la base de datos
    con el estado Waiting."""
    db = base.SessionLocal()
    games = db.query(GameTable).filter(GameTable.state == "Waiting").all()
    game_list: List[Game] = []
    for g in games:
        game_list.append(Game(id=g.id, name=g.name, state=g.state,
                              turn=g.turn, host=g.host, players=g.players,
                              max_players=g.max_players, min_players=g.min_players,
                              password=g.password))
    return game_list

def set_game_state(id_game: int, state: str):
    db = base.SessionLocal()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.state: state})
    db.commit()

def set_game_turn(id_game: int, turn: int):
    db = base.SessionLocal()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.turn: turn})
    db.commit()

#Alguna para el timer?