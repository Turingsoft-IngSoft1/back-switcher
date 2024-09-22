from models import base
from models import game
from schemas import game_schema

def create_game(
                name: str, 
                host: str,
                max_players: int, 
                min_players: int):
    
    db = base.SessionLocal()
    
    try:
        new_game = game.GameTable(
                        name=name, 
                        host=host, 
                        max_players=max_players, 
                        min_players=min_players)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        print(f"Game {new_game.id} created")
    except Exception as e:
        db.rollback()
        print(f"Error creating game: {e}")
    finally:
        db.close()

def get_game(id_game: int) -> game_schema.Game:
    db = base.SessionLocal()
    gameRet = db.query(game).filter(game.id == id_game).first()
    return game_schema.Game(
                                id=gameRet.id,
                                name=gameRet.name,
                                state=gameRet.state,
                                turn=gameRet.turn,
                                host=gameRet.host,
                                players=gameRet.players,
                                max_players=gameRet.max_players,
                                min_players=gameRet.min_players,
                                password=gameRet.password,
                                timer=gameRet.timer)
    
def list_games() -> list[int, game_schema.Game]:
    db = base.SessionLocal()
    games = db.query(game).filter(game.state == "Waiting").all()
    game_list = []
    for game in games:
        game_list.append(game_schema.Game(
                                            id=game.id,
                                            name=game.name,
                                            state=game.state,
                                            turn=game.turn,
                                            host=game.host,
                                            players=game.players,
                                            max_players=game.max_players,
                                            min_players=game.min_players,
                                            password=game.password,
                                            timer=game.timer))
        
    return game_list

def set_game_state(id_game: int, state: str):
    db = base.SessionLocal()
    db.query(game.GameTable).filter(game.GameTable.id == id_game).update({game.GameTable.state: state})
    db.commit()

def set_game_turn(id_game: int, turn: int):
    db = base.SessionLocal()
    db.query(game.GameTable).filter(game.GameTable.id == id_game).update({game.GameTable.turn: turn})
    db.commit()

#Alguna para el timer?