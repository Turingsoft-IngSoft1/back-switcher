from models import base
from models.game import GameTable
from schemas import game_schema


def create_game(name: str, max_players: int, min_players: int):
    """Crea una partida y la inserta en la base de datos."""
    db = base.SessionLocal()
    try:
        new_game = GameTable(name=name,
                             max_players=max_players,
                             min_players=min_players)
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


def get_game(id_game: int) -> game_schema.Game:
    """Encuentra y muestra el juego que esta almacenado
    en la base de datos con el respectivo id."""
    db = base.SessionLocal()
    game_ret = db.query(GameTable).filter(GameTable.id == id_game).first()
    return game_schema.Game(id=game_ret.id,
                            name=game_ret.name,
                            state=game_ret.state,
                            turn=game_ret.turn,
                            host=game_ret.host,
                            players=game_ret.players,
                            max_players=game_ret.max_players,
                            min_players=game_ret.min_players,
                            password=game_ret.password,
                            moves_deck=game_ret.moves_deck)


def listing_games() -> list[game_schema.Game]:
    """Devuelve la lista de las partidas en la base de datos
    con el estado Waiting."""
    db = base.SessionLocal()
    games = db.query(GameTable).filter(GameTable.state == "Waiting").all()
    game_list = []
    for game in games:
        game_list.append(game_schema.Game(id=game.id,
                                          name=game.name,
                                          state=game.state,
                                          turn=game.turn,
                                          host=game.host,
                                          players=game.players,
                                          max_players=game.max_players,
                                          min_players=game.min_players,
                                          password=game.password,
                                          moves_deck=game.moves_deck))
    return game_list


def set_game_state(id_game: int, state: str):
    db = base.SessionLocal()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.state: state})
    db.commit()


def set_game_turn(id_game: int, turn: int):
    db = base.SessionLocal()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.turn: turn})
    db.commit()


def set_game_host(id_game: int, host: int):
    db = base.SessionLocal()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.host: host})
    db.commit()


def get_players(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.players


def get_max_players(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.max_players

def get_min_players(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.min_players

def get_game_state(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.state

def get_game_turn(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.turn

def add_player(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.players: tab.players + 1})
    db.commit()


def remove_player(id_game: int):
    db = base.SessionLocal()
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.players: tab.players - 1})
    db.commit()


def remove_game(id_game: int):
    """Elimina de la base de datos la partida con el id correspondiente."""
    db = base.SessionLocal()
    to_remove = db.query(GameTable).filter(GameTable.id == id_game).first()
    try:
        db.delete(to_remove)
        db.commit()
        print(f"Game deleted.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
