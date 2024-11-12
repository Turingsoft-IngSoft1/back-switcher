import random
from pytest import MonkeyPatch
from querys import create_game,create_user,remove_game
from querys.move_queries import *
from models import MoveTable

def mock_shuffle(x):
    """Mock para que la funcion shuffle no se aplique."""
    
def test_initialize_moves(monkeypatch,test_db):
    """Testea la inicializacion de los movimientos."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    #Caso 1: 2 jugadores
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)

    initialize_moves(1,2,test_db)

    count = test_db.query(MoveTable).filter_by(id_game=1).count()
    assert count == 49
    count = test_db.query(MoveTable).filter_by(id_game=1,status="Deck").count()
    assert count == 49-(3*2)
    count = test_db.query(MoveTable).filter_by(id_game=1,status="InHand").count()
    assert count == 3*2
    h1 = get_hand(1,1,test_db)
    h2 = get_hand(1,2,test_db)
    assert len(h1) == 3 and len(h2) == 3
    assert h1 == ['mov1','mov2','mov3'] and h2 == ['mov4','mov5','mov6']
    
    remove_game(1,test_db)

    #Caso 2: 3 jugadores
    newid=create_game("game1",2,3,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    create_user("user3",newid,test_db)
    initialize_moves(1,3,test_db)

    count = test_db.query(MoveTable).filter_by(id_game=1,status="Deck").count()
    assert count == 49-(3*3)
    count = test_db.query(MoveTable).filter_by(id_game=1,status="InHand").count()
    assert count == 3*3
    h1 = get_hand(1,1,test_db)
    h2 = get_hand(1,2,test_db)
    h3 = get_hand(1,3,test_db)
    assert len(h1) == 3 and len(h2) == 3 and len(h3) == 3
    assert (h1 == ['mov1','mov2','mov3'] and
            h2 == ['mov4','mov5','mov6'] and
            h3 == ['mov7','mov1','mov2'])
    
    remove_game(1,test_db)

    #Caso 3: 4 jugadores
    newid=create_game("game1",2,4,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    create_user("user3",newid,test_db)
    create_user("user4",newid,test_db)
    initialize_moves(1,4,test_db)

    count = test_db.query(MoveTable).filter_by(id_game=1,status="Deck").count()
    assert count == 49-(3*4)
    count = test_db.query(MoveTable).filter_by(id_game=1,status="InHand").count()
    assert count == 3*4
    h1 = get_hand(1,1,test_db)    
    h2 = get_hand(1,2,test_db)
    h3 = get_hand(1,3,test_db)
    h4 = get_hand(1,4,test_db)
    assert len(h1) == 3 and len(h2) == 3 and len(h3) == 3 and len(h4) == 3
    assert (h1 == ['mov1','mov2','mov3'] and
            h2 == ['mov4','mov5','mov6'] and
            h3 == ['mov7','mov1','mov2'] and
            h4 == ['mov3','mov4','mov5'])

def test_moves_in_deck(monkeypatch,test_db):
    """Testea la cantidad de movimientos en el mazo."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    count1 = moves_in_deck(1,test_db)
    count2 = test_db.query(MoveTable).filter_by(id_game=1,status="Deck").count()
    assert count1 == count2 == 49-(3*2)
    remove_game(1,test_db)

def test_moves_in_hand(monkeypatch,test_db):
    """Testea la cantidad de movimientos en la mano de un jugador."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    count1 = moves_in_hand(1,1,test_db)
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status="InHand").count()
    assert count1 == count2 == 3
    count1 = moves_in_hand(1,2,test_db)
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=2,status="InHand").count()
    assert count1 == count2 == 3
    remove_game(1,test_db)

def test_refill_moves(monkeypatch,test_db):
    """Testea devolver los movimientos descartados al mazo."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    test_db.query(MoveTable).filter_by(id_game=1,status='Deck').first().status = 'Discarded'
    test_db.query(MoveTable).filter_by(id_game=1,status='Deck').first().status = 'Discarded'
    test_db.commit()    
    count1 = test_db.query(MoveTable).filter_by(id_game=1,status='Discarded').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,status='Deck').count()
    assert count1 == 2 and count2 == 49-(3*2)-2
    refill_moves(1,test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,status='Discarded').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,status='Deck').count()
    assert count1 == 0 and count2 == 49-(3*2)
    remove_game(1,test_db)

def test_refill_hand(monkeypatch,test_db):
    """Testea rellenar la mano del jugador."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').first().status = 'Discarded'
    test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').first().status = 'Discarded'
    test_db.commit()
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 2 and count2 == 1
    refill_hand(1,1,2,test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 2 and count2 == 3
    remove_game(1,test_db)

def test_get_hand(monkeypatch,test_db):
    """Testea que se devuelvan los nombres de los movimientos en la mano del jugador."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    #Caso 1: Los usuarios no han descartado cartas.
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    h1 = get_hand(1,1,test_db)
    h2 = get_hand(1,2,test_db)
    assert len(h1) == 3 and len(h2) == 3
    assert h1 == ['mov1','mov2','mov3'] and h2 == ['mov4','mov5','mov6']
    
    #Caso 2: Los usuarios han descartado algunas cartas.
    test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').first().status = 'Discarded'
    test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').first().status = 'Discarded'
    test_db.query(MoveTable).filter_by(id_game=1,id_user=2,status='InHand').first().status = 'Discarded'
    test_db.commit()
    h1 = get_hand(1,1,test_db)
    h2 = get_hand(1,2,test_db)
    assert len(h1) == 1 and len(h2) == 2
    assert h1 == ['mov3'] and h2 == ['mov5','mov6']

def test_use_move(monkeypatch, test_db):
    """Testea que se utilicen los movimientos."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Played').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 0 and count2 == 3
    use_move(1,1,"mov1",test_db)
    use_move(1,1,"mov3",test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Played').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 2 and count2 == 1
    
def test_unplay_moves(monkeypatch, test_db):
    """Testea devolver los movimientos jugados a la mano del jugador."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    use_move(1,1,"mov1",test_db)
    use_move(1,1,"mov3",test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Played').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 2 and count2 == 1
    unplay_moves(1, test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Played').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 0 and count2 == 3
    
def test_get_played(monkeypatch, test_db):
    """Testea que devuelva la cantidad de cartas jugadas."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    use_move(1,1,"mov1",test_db)
    use_move(1,1,"mov3",test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Played').count()
    assert count1 == 2 == get_played(1,test_db)
    
def test_discard_move(monkeypatch, test_db):
    """Testea que se descarten los movimientos."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 0 and count2 == 3
    use_move(1,1,"mov1",test_db)
    use_move(1,1,"mov3",test_db)
    discard_move(1,1,test_db)
    count1 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Discarded').count()
    count2 = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='InHand').count()
    assert count1 == 2 and count2 == 1
    
def test_get_partial_moves(monkeypatch, test_db):
    """Testea que devuelva las cartas jugadas."""
    
    monkeypatch.setattr('querys.move_queries.shuffle', mock_shuffle)
    
    newid=create_game("game1",2,2,"",test_db)
    create_user("user1",newid,test_db)
    create_user("user2",newid,test_db)
    initialize_moves(1,2,test_db)
    use_move(1,1,"mov1",test_db)
    use_move(1,1,"mov3",test_db)
    moves = test_db.query(MoveTable).filter_by(id_game=1,id_user=1,status='Played').all()
    i = 0
    for move in moves:
        assert move.name == get_partial_moves(1,1,test_db)[i]
        i+=1