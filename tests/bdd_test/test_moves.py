import pytest
from querys.move_queries import *
from models import MoveTable
from sqlite3 import IntegrityError

def test_create_move(test_db, force_teardown):
    
    #Caso 1: Crear un movimiento correctamente.
    create_move("mov1", id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab is not None
    
    #Caso 2: Se crea otro movimiento con el mismo nombre.
    create_move("mov1", id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).all()
    assert tab is not None
    
    assert tab[0].name == tab[1].name
    assert tab[0].id != tab[1].id
    assert tab[0].id_game == tab[1].id_game
    
    #Caso 3: Crear movimiento con un nombre incorrecto.
    try:
        id = create_move("InvalidMove", id_game=1, db=test_db)
    except IntegrityError:
        pass
    tab = test_db.query(MoveTable).filter_by(id=id).first()
    assert tab == None
       
def test_set_move_user(test_db, force_teardown):
    
    #Se le asigna a un jugador.
    id = create_move("mov1", id_game=1, db=test_db)
    set_move_user(id, 1, test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.user_id is not None
    
def test_get_move_user(test_db, force_teardown):
    
    #Caso 1: No pertenece a ningun jugador todavia.
    id = create_move("mov1", id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.user_id == None == get_move_user(id, test_db)
    
    #Caso 2: Pertenece a un jugador.
    set_move_user(id, 1, test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.user_id == 1 == get_move_user(id, test_db)
    
def test_get_move_name(test_db, force_teardown):
    
    #Obtiene el nombre del movimiento.
    id = create_move("mov1", id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id=id).first()
    assert tab.name == "mov1" == get_move_name(id, test_db) 
    
def test_get_move_status(test_db, force_teardown):
    
    #Obtiene el status actual de la carta.
    id = create_move("mov1", id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.status == "Deck" == get_move_status(id, test_db)
    
def test_set_move_status(test_db, force_teardown):
    
    #Caso 1: Asigna la carta a la mano de un jugador
    id = create_move("mov1", id_game=1, db=test_db)
    set_move_status(id, "InHand", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.status == "InHand"
    
    #Caso 2: Asigna la carta a el status de descarte
    set_move_status(id, "Discarded", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.status == "Discarded"
    
    #Caso 3: Asigna la carta al deck
    set_move_status(id, "Deck", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.status == "Deck"
    
    #Caso 4: Se asigna un status incorrectamente.
    try:
        set_move_status(id, "InvalidStatus", test_db)
    except IntegrityError:
        pass
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.status == "Deck"
    
def test_get_deck(test_db, force_teardown):
    
    #Obtiene el id de los movimientos en deck
    
    #Caso 1: Hay movimientos en deck
    temp = []
    for i in range(1, 8):
        temp.append(create_move(f"mov{i}", id_game=1, db=test_db))
    tab = temp
    assert tab == get_deck(id_game=1, db=test_db)
    
    #Caso 2: No quedan movimientos en deck
    for i in temp:
        set_move_status(i, "Discarded", test_db)
    assert get_deck(id_game=1, db=test_db) == []

def test_moves_in_deck(test_db, force_teardown):
    
    #Obtiene la cantidad de movimientos en deck
    
    #Caso 1: Hay movimientos en deck
    temp = []
    for i in range(1, 8):
        temp.append(create_move(f"mov{i}", id_game=1, db=test_db))
    tab = test_db.query(MoveTable).filter_by(id_game=1, status="Deck").count()
    assert tab == 7 == moves_in_deck(id_game=1, db=test_db)
    
    #Caso 2: No quedan movimientos en deck
    for i in temp:
        set_move_status(i, "Discarded", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1, status="Deck").count()
    assert tab == 0 == moves_in_deck(id_game=1, db=test_db)

def test_moves_in_hand(test_db, force_teardown):
    #Obtiene la cantidad de movimientos en la mano de un jugador
    
    #Caso 1: No tiene movimientos en su mano
    temp = []
    for i in range(1, 4):
        temp.append(create_move(f"mov{i}", id_game=1, db=test_db))
    tab = test_db.query(MoveTable).filter_by(id_game=1, status="InHand").count()
    assert tab == 0 == moves_in_hand(id_game=1, user_id=1, db=test_db)
    
    #Caso 2: Tiene movimientos en su mano
    for i in temp:
        set_move_status(i, "InHand", test_db)
        set_move_user(i, user_id=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1, status="InHand").count()
    assert tab == 3 == moves_in_hand(id_game=1, user_id=1, db=test_db)

def test_refill_moves(test_db, force_teardown):
     
    #Devuelve todos los movimientos descartados al mazo.
    
    #Caso 1: No hay movimientos descartados
    temp = []
    for i in range(1, 8):
        temp.append(create_move(name=f"mov{i}", id_game=1, db=test_db))
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Discarded").first()
    assert tab == None
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Deck").first()
    assert tab is not None
    refill_moves(id_game=1, db=test_db)
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Discarded").first()
    assert tab == None
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Deck").first()
    assert tab is not None
    
    #Caso 2: Hay movimientos descartados.
    for i in temp:
        set_move_status(i, "Discarded", test_db)
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Discarded").first()
    assert tab is not None
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Deck").first()
    assert tab == None
    refill_moves(id_game=1, db=test_db)
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Discarded").first()
    assert tab == None
    tab = tab = test_db.query(MoveTable).filter_by(id_game=1, status="Deck").first()
    assert tab is not None
    
def test_remove_move(test_db, force_teardown):
    
    #Caso 1: Se elimina una carta de movimiento existente.
    id = create_move("mov1", id_game=1, db=test_db)
    remove_move(id, test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab == None
    
    #Caso 2: Se elimina una carta de movimiento inexistente.
    id = None
    remove_move(id, test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab == None
    
def test_initialize_moves(test_db, force_teardown):
    
    #Inicializa las cartas de movimientos.
    initialize_moves(id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab is not None