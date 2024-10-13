import random
from pytest import MonkeyPatch
from querys.figure_queries import *
from querys import create_game,create_user,remove_game
from models import FigureTable,UserTable

def test_initialize_figures(monkeypatch,test_db):
    """Testea la inicializacion de las figuras."""
    def mock_shuffle(x):
        pass
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,test_db)
    id1 = create_user("user1",newid,test_db)
    id2 = create_user("user2",newid,test_db)
    initialize_figures(newid,2,test_db)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Hidden").count() == (50-3*2)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",user_id=id1).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",user_id=id2).count() == 3
    remove_game(newid,test_db)

def test_get_revealed_figures(monkeypatch,test_db):
    """Testea la inicializacion de las figuras."""
    def mock_shuffle():
        pass
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    test_db.query(UserTable).filter_by(id=u2).update({"turn":1})
    initialize_figures(newid,2,test_db)
    revealed = get_revealed_figures(newid,test_db)
    print(revealed)
    assert len(revealed[u1]) == 3 and len(revealed[u2]) == 3
    remove_game(newid,test_db)
