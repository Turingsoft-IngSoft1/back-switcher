import pytest
from querys import game_queries
from models import GameTable
from schemas.game_schema import Game
from sqlite3 import IntegrityError

def test_create_game(test_db):
    try:
        game_id = game_queries.create_game("Draken", 4, 2, "", test_db)
        game = test_db.query(GameTable).filter_by(id=game_id).first()
        assert game is not None
        assert game_id == game.id
        assert game.state == "Waiting"
        assert game.name == "Draken"
        assert game.min_players == 2
        assert game.max_players == 4
        assert game.password == ""

    except IntegrityError:
        pass
    
def test_get_game(test_db):
    try:
        game_id = game_queries.create_game("Europas evija hjarta", 4, 2, "", test_db)
        game = test_db.query(GameTable).filter_by(id=game_id).first()
        assert game_queries.get_game(game_id, test_db) == Game(id=1,
                                                               name='Europas evija hjarta',
                                                               state='Waiting',
                                                               turn=0,
                                                               host=0,
                                                               players=1,
                                                               max_players=4,
                                                               min_players=2,
                                                               password="",
                                                               private=False)
    except IntegrityError:
        pass

def test_set_game_state(test_db):
    
    game_id = game_queries.create_game("Genom Sverige i tiden", 3, 2, "", test_db)
        
    game_queries.set_game_state(game_id, "Playing", test_db)
    game = test_db.query(GameTable).filter_by(id=game_id).first()
    assert game.state == "Playing"
        
    game_queries.set_game_state(game_id, "Finished", test_db)
    game = test_db.query(GameTable).filter_by(id=game_id).first()
    assert game.state == "Finished"

    #Caso de error: Setear un estado inválido
    try:
        game_queries.set_game_state(game_id, "Marcus Wandt", test_db)
        assert game.state == "Marcus Wandt"
    except IntegrityError:
        pass

def test_get_game_state(test_db):
    try:
        game_id = game_queries.create_game("Västkustens styrka och stolthet", 3, 2, "", test_db)
        game_queries.set_game_state(game_id, "Playing", test_db)
        game = test_db.query(GameTable).filter_by(id=game_id).first()
        assert game.state == "Playing"
    except IntegrityError:
        pass

def test_listing_games(test_db): #Chequear
    try:
        game_id = game_queries.create_game("Gottland regemente", 3, 2, "", test_db)
        game_id2 = game_queries.create_game("Skaraborgs regemente", 4, 2, "", test_db)
        game_id3 = game_queries.create_game("Uppland regemente", 2, 2, "", test_db)
        games = test_db.query(GameTable).all()
        assert game_queries.listing_games(test_db) == [Game(id=1,
                                                            name='Gottland regemente',
                                                            state='Waiting',
                                                            turn=0, host=0,
                                                            players=1,
                                                            max_players=3,
                                                            min_players=2,
                                                            password="False", 
                                                            private=False),
                                                       Game(id=2,
                                                            name='Skaraborgs regemente',
                                                            state='Waiting',
                                                            turn=0,
                                                            host=0,
                                                            players=1,
                                                            max_players=4,
                                                            min_players=2,
                                                            password="False",
                                                            private=False),
                                                       Game(id=3,
                                                            name='Uppland regemente',
                                                            state='Waiting',
                                                            turn=0,
                                                            host=0,
                                                            players=1,
                                                            max_players=2,
                                                            min_players=2,
                                                            password="False",
                                                            private=False)]
    except IntegrityError:
        pass

def test_set_game_turn(test_db):
    
    game_id = game_queries.create_game("Scania regemente", 3, 2, "", test_db)
    game = test_db.query(GameTable).filter_by(id=game_id).first()
        
    game_queries.set_game_turn(game_id, 2, test_db)
    game = test_db.query(GameTable).filter_by(id=game_id).first()
    assert game.turn == 2
        
    game_queries.set_game_turn(game_id, 3, test_db)
    game = test_db.query(GameTable).filter_by(id=game_id).first()
    assert game.turn == 3
        
    game_queries.set_game_turn(game_id, 1, test_db)
    game = test_db.query(GameTable).filter_by(id=game_id).first()
    assert game.turn == 1
    
    try:
        #Caso de error: Setear un turno inválido (jugador inválido)
        game_queries.set_game_turn(game_id, 4, test_db)
        assert game.turn == 4

        game_queries.set_game_turn(game_id, -1, test_db)
        assert game.turn == -1

    except IntegrityError:
        pass

def test_get_game_turn(test_db):
    try:
        game_id = game_queries.create_game("Blekinge regemente", 3, 2, "", test_db)
        game_queries.set_game_turn(game_id, 2, test_db)
        assert game_queries.get_game_turn(game_id, test_db) == 2
        game_queries.set_game_turn(game_id, 3, test_db)
        assert game_queries.get_game_turn(game_id, test_db) == 3

    except IntegrityError:
        pass

#Chequear
def test_set_game_host(test_db):
    try:
        game_id = game_queries.create_game("Jämtland regemente", 3, 2, "", test_db)
        game = test_db.query(GameTable).filter_by(id=game_id).first()
        game_queries.set_game_host(game_id, 2, test_db)
        assert game.host == 2
        game_queries.set_game_host(game_id, 3, test_db)
        assert game.host == 3
        game_queries.set_game_host(game_id, 1, test_db)
        assert game.host == 1
    except IntegrityError:
        pass

def test_get_players(test_db):
    try:
        game_id = game_queries.create_game("Värmlands regemente", 3, 2, "", test_db)
        game_queries.add_player(game_id, test_db)
        game_queries.add_player(game_id, test_db)
        assert game_queries.get_players(game_id, test_db) == 3
        game_queries.remove_player(game_id, test_db)
        assert game_queries.get_players(game_id, test_db) == 2

    except IntegrityError:
        pass

def test_get_max_players(test_db):
    try:
        game_id1 = game_queries.create_game("Alvsborg regemente", 3, 2, "", test_db)
        game_id2 = game_queries.create_game("Dalregemente", 4, 2, "", test_db)
        assert game_queries.get_max_players(game_id1, test_db) == 3
        assert game_queries.get_max_players(game_id2, test_db) == 4
    except IntegrityError:
        pass

def test_get_min_players(test_db):
    try:
        game_id1 = game_queries.create_game("Hallands regemente", 3, 2, "", test_db)
        game_id2 = game_queries.create_game("Västgöta regemente", 4, 3, "", test_db)
        assert game_queries.get_min_players(game_id1, test_db) == 2
        assert game_queries.get_min_players(game_id2, test_db) == 3
    except IntegrityError:
        pass

def test_add_player(test_db):
    try:
        game_id = game_queries.create_game("Gotlands regemente", 3, 2, "", test_db)
        game_queries.add_player(game_id, test_db)
        assert game_queries.get_players(game_id, test_db) == 2
        game_queries.add_player(game_id, test_db)
        assert game_queries.get_players(game_id, test_db) == 3
        game_queries.add_player(game_id, test_db)
        assert game_queries.get_players(game_id, test_db) == 4
    except IntegrityError:
        pass

def test_remove_player(test_db):
    game_id = game_queries.create_game("Gotlands regemente", 3, 2, "", test_db)
    game_queries.add_player(game_id, test_db)
    game_queries.add_player(game_id, test_db)
    game_queries.add_player(game_id, test_db)
    game_queries.remove_player(game_id, test_db)
    assert game_queries.get_players(game_id, test_db) == 3
    game_queries.remove_player(game_id, test_db)
    assert game_queries.get_players(game_id, test_db) == 2
    game_queries.remove_player(game_id, test_db)
    assert game_queries.get_players(game_id, test_db) == 1
    
    try:
        #Caso de error: Intentar sacar a un jugador de una partida vacía.
        game_queries.remove_player(game_id, test_db)
    
    except IntegrityError:
        pass

def test_remove_game(test_db):
    try:
        game_id = game_queries.create_game("Gotlands regemente", 3, 2, "", test_db)
        game_queries.remove_game(game_id, test_db)
        assert test_db.query(GameTable).filter_by(id=game_id).first() is None
    except IntegrityError:
        pass
