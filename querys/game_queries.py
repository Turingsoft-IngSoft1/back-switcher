from sqlalchemy.exc import SQLAlchemyError
from models.game import GameTable
from schemas import game_schema


def create_game(name: str, max_players: int, min_players: int, db): #Tested
    """Crea una partida y la inserta en la base de datos."""
    try:
        new_game = GameTable(name=name,
                             max_players=max_players,
                             min_players=min_players)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        print(f"Game {new_game.id} created")
        return new_game.id
    except SQLAlchemyError as e: #pragma: no cover
        db.rollback() #pragma: no cover
        print(f"Error creating game: {e}") #pragma: no cover


def get_game(id_game: int, db) -> game_schema.Game: #Tested
    """Encuentra y muestra el juego que esta almacenado
    en la base de datos con el respectivo id."""
    if db.query(GameTable).filter(GameTable.id == id_game).count() != 0:
        
        game_ret = db.query(GameTable).filter(GameTable.id == id_game).first()
        return game_schema.Game(id=game_ret.id,
                                name=game_ret.name,
                                state=game_ret.state,
                                turn=game_ret.turn,
                                host=game_ret.host,
                                players=game_ret.players,
                                max_players=game_ret.max_players,
                                min_players=game_ret.min_players,
                                password=game_ret.password)
    else:
        return None

def listing_games(db) -> list[game_schema.Game]: #Tested
    """Devuelve la lista de las partidas en la base de datos
    con el estado Waiting."""
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
                                          password=game.password))
    return game_list


def set_game_state(id_game: int, state: str, db): #Tested
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.state: state})
    db.commit()


def set_game_turn(id_game: int, turn: int, db): #Tested
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.turn: turn})
    db.commit()


def set_game_host(id_game: int, host: int, db): #Tested
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.host: host})
    db.commit()


def get_players(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.players


def get_max_players(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.max_players

def get_min_players(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.min_players

def get_game_state(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.state

def get_game_turn(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    return tab.turn

def add_player(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.players: tab.players + 1})
    db.commit()

def remove_player(id_game: int, db): #Tested
    tab = db.query(GameTable).filter(GameTable.id == id_game).first()
    db.query(GameTable).filter(GameTable.id == id_game).update({GameTable.players: tab.players - 1})
    db.commit()


def remove_game(id_game: int, db): 
    """Elimina de la base de datos la partida con el id correspondiente."""
    to_remove = db.query(GameTable).filter(GameTable.id == id_game).first()
    try:
        db.delete(to_remove)
        db.commit()
        print(f"Game deleted.")
    except SQLAlchemyError as e: #pragma: no cover
        db.rollback() #pragma: no cover
        print(f"Error: {e}") #pragma: no cover
    
