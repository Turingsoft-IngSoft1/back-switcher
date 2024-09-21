from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Game  

engine = create_engine('sqlite:///game.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_game_status(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first()

def get_game_name(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().name

def get_game_state(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().state

def get_game_turn(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().turn

def get_game_host(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().host

def get_game_max_players(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().max_players

def get_game_min_players(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().min_players

def get_game_password(db: Session, id_game: int):
    return db.query(Game).filter(Game.id == id_game).first().password

def set_game_state(db: Session, id_game: int, state: str):
    db.query(Game).filter(Game.id == id_game).update({Game.state: state})
    db.commit()

def set_game_turn(db: Session, id_game: int, turn: int):
    db.query(Game).filter(Game.id == id_game).update({Game.turn: turn})
    db.commit()

def set_game_host(db: Session, id_game: int, host: str):
    db.query(Game).filter(Game.id == id_game).update({Game.host: host})
    db.commit()

def set_game_max_players(db: Session, id_game: int, max_players: int):
    db.query(Game).filter(Game.id == id_game).update({Game.max_players: max_players})
    db.commit()

def set_game_min_players(db: Session, id_game: int, min_players: int):
    db.query(Game).filter(Game.id == id_game).update({Game.min_players: min_players})
    db.commit()

def set_game_password(db: Session, id_game: int, password: str):
    db.query(Game).filter(Game.id == id_game).update({Game.password: password})
    db.commit()



#Alguna para el timer?