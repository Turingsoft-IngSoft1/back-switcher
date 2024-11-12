import random
from pytest import MonkeyPatch
from querys.figure_queries import *
from querys import create_game,create_user,remove_game
from models import FigureTable,UserTable
from models.figure import figures

def check_valid(revealed):
    """Chequea que las figuras reveladas sean validas."""
    for r in revealed:
        if r not in figures:
            return False
    return True

def mock_shuffle(x):
    """Mock para que la funcion shuffle no se aplique."""

def test_initialize_figures(monkeypatch,test_db):
    """Testea la inicializacion de las figuras."""

    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    #Caso 1: 2 jugadores
    newid = create_game("game1",2,2,"",test_db)
    id1 = create_user("user1",newid,test_db)
    id2 = create_user("user2",newid,test_db)
    test_db.query(UserTable).filter_by(id=id2).update({"turn":1})
    initialize_figures(newid,2,test_db)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Hidden").count() == (50-3*2)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id1).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id2).count() == 3
    remove_game(newid,test_db)
    
    #Caso 2: 3 jugadores
    newid = create_game("game1",2,3,"",test_db)
    id1 = create_user("user1",newid,test_db)
    id2 = create_user("user2",newid,test_db)
    id3 = create_user("user3",newid,test_db)
    test_db.query(UserTable).filter_by(id=id3).update({"turn":1})
    initialize_figures(newid,3,test_db)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Hidden").count() == (50-3*3)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id1).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id2).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id3).count() == 3
    remove_game(newid,test_db)
    
    #Caso 3: 4 jugadores
    newid = create_game("game1",2,4,"",test_db)
    id1 = create_user("user1",newid,test_db)
    id2 = create_user("user2",newid,test_db)
    id3 = create_user("user3",newid,test_db)
    id4 = create_user("user4",newid,test_db)
    test_db.query(UserTable).filter_by(id=id4).update({"turn":1})
    initialize_figures(newid,4,test_db)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Hidden").count() == (50-3*4)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id1).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id2).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id3).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=id4).count() == 3
    remove_game(newid,test_db)

def test_get_revealed_figures(monkeypatch,test_db):
    """Testea obtener figuras reveladas."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    test_db.query(UserTable).filter_by(id=u2).update({"turn":1})
    initialize_figures(newid,2,test_db)
    revealed = get_revealed_figures(newid,test_db)
    assert len(revealed[u1]) == 3 and len(revealed[u2]) == 3
    assert check_valid(revealed[u1]) and check_valid(revealed[u2])
    remove_game(newid,test_db)

def test_get_blocked_figures(monkeypatch,test_db):
    """Testea obtener figuras bloqueadas."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    test_db.query(UserTable).filter_by(id=u2).update({"turn":1})
    initialize_figures(newid,2,test_db)
    figures = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').all()
    block_figure(1,1,figures[0].name,test_db)
    blocked = get_blocked_figures(newid,test_db)
    assert len(blocked[u1]) == 1
    assert check_valid(blocked[u1]) and check_valid(blocked[u2])
    remove_game(newid,test_db)

def test_refill_revealed_figures(monkeypatch,test_db):
    """Testea el repartir nuevas cartas de figuras para el jugador."""
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,4,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    u3 = create_user("user3",newid,test_db)
    u4 = create_user("user4",newid,test_db)
    test_db.query(UserTable).filter_by(id=u2).update({"turn":1})
    test_db.query(UserTable).filter_by(id=u3).update({"turn":2})
    test_db.query(UserTable).filter_by(id=u4).update({"turn":3})
    initialize_figures(newid,4,test_db)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Hidden").count() == (50-3*4)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u1).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u2).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u3).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u4).count() == 3
    test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u1).first().status = "Discarded"
    test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u2).first().status = "Discarded"
    test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u3).first().status = "Discarded"
    test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u3).first().status = "Discarded"
    test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u3).first().status = "Discarded"
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u1).count() == 2
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u2).count() == 2
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u3).count() == 0
    refill_revealed_figures(newid,u1,test_db)
    refill_revealed_figures(newid,u2,test_db)
    refill_revealed_figures(newid,u3,test_db)
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u1).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u2).count() == 3
    assert test_db.query(FigureTable).filter_by(id_game=newid,status="Revealed",id_user=u3).count() == 3
    revealed = get_revealed_figures(newid,test_db)
    assert len(revealed[u1]) == 3 and len(revealed[u2]) == 3 and len(revealed[u3]) == 3
    assert check_valid(revealed[u1]) and check_valid(revealed[u2]) and check_valid(revealed[u3])
    remove_game(newid,test_db)

def test_figures_in_hand(monkeypatch,test_db):
    """Testea la cantidad de figuras en mano."""
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    test_db.query(UserTable).filter_by(id=u2).update({"turn":1})
    initialize_figures(newid,2,test_db)
    assert figures_in_hand(newid,u1,test_db) == 3
    assert figures_in_hand(newid,u2,test_db) == 3
    remove_game(newid,test_db)
    
def test_use_figure(monkeypatch, test_db):
    """Testea que se utilicen las figuras."""
    
    monkeypatch.setattr('querys.figure_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_figures(1,2,test_db)
    count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').count()
    count2 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    assert count1 == 3 and count2 == 0
    figures = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').all()
    use_figure(1,1,figures[0].name,test_db)
    use_figure(1,1,figures[1].name,test_db)
    count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').count()
    count2 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    assert count1 == 1 and count2 == 2
    
def test_block_figure(monkeypatch, test_db):
    """Testea que se bloqueen las figuras."""
    
    monkeypatch.setattr('querys.figure_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_figures(1,2,test_db)
    count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').count()
    count2 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Blocked').count()
    assert count1 == 3 and count2 == 0
    figures = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').all()
    block_figure(1,1,figures[0].name,test_db)
    count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').count()
    count2 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Blocked').count()
    assert count1 == 2 and count2 == 1

def test_figures_in_deck(monkeypatch,test_db):
    """Testea la cantidad de figuras en el mazo."""
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    #Caso 1: 2 jugadores.
    newid = create_game("game1",2,2,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    test_db.query(UserTable).filter_by(id=u2).update({"turn":1})
    initialize_figures(newid,2,test_db)
    assert figures_in_deck(newid,u1,test_db) == 22
    assert figures_in_deck(newid,u2,test_db) == 22
    remove_game(newid,test_db)
    
    #Caso 2: 3 jugadores.
    newid = create_game("game1",2,3,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    u3 = create_user("user3",newid,test_db)
    test_db.query(UserTable).filter_by(id=u3).update({"turn":1})
    initialize_figures(newid,3,test_db)
    assert figures_in_deck(newid,u1,test_db) == 13
    assert figures_in_deck(newid,u2,test_db) == 14
    assert figures_in_deck(newid,u3,test_db) == 14
    remove_game(newid,test_db)
    
    #Caso 3: 4 jugadores.
    newid = create_game("game1",2,4,"",test_db)
    u1 = create_user("user1",newid,test_db)
    u2 = create_user("user2",newid,test_db)
    u3 = create_user("user3",newid,test_db)
    u4 = create_user("user4",newid,test_db)
    test_db.query(UserTable).filter_by(id=u4).update({"turn":1})
    initialize_figures(newid,4,test_db)
    assert figures_in_deck(newid,u1,test_db) == 9
    assert figures_in_deck(newid,u2,test_db) == 10
    assert figures_in_deck(newid,u3,test_db) == 10
    assert figures_in_deck(newid,u4,test_db) == 9

    remove_game(newid,test_db)

def test_blocked_figure(test_db, monkeypatch):
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,"",test_db)
    u_id = create_user("user1", newid, test_db)
    create_user("user2", newid, test_db)
    initialize_figures(newid, 2, test_db)
    rf = get_revealed_figures(newid, test_db)[u_id]
    block_figure(newid, u_id, rf[0], test_db)

    assert  is_user_blocked(newid, u_id, test_db)
    
def test_unblock_figure(test_db, monkeypatch):
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)

    newid = create_game("game1",2,2,"",test_db)
    u_id = create_user("user1", newid, test_db)
    create_user("user2", newid, test_db)
    initialize_figures(newid, 2, test_db)
    rf = get_revealed_figures(newid, test_db)[u_id]
    block_figure(newid, u_id, rf[0], test_db)

    use_figure(newid, u_id, rf[1], test_db)
    use_figure(newid, u_id, rf[2], test_db)

    unblock_figure(newid, u_id, test_db)

    assert  not is_user_blocked(newid, u_id, test_db)
    
def test_use_move(monkeypatch, test_db):
    """Testea que se utilicen las figuras."""
    
    monkeypatch.setattr('querys.figure_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_figures(1,2,test_db)
    count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').count()
    count2 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    assert count1 == 3 and count2 == 0
    figures = count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').all()
    use_figure(1,1,figures[0].name,test_db)
    use_figure(1,1,figures[1].name,test_db)
    count1 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Revealed').count()
    count2 = test_db.query(FigureTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    assert count1 == 1 and count2 == 2
