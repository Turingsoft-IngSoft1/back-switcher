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
    
    #Caso 3: Crear movimiento incorrectamente.
    #Falta implementar una validacion del nombre de los movimientos en models.
    
def test_get_move_pile(test_db, force_teardown):
    
    #Obtiene la pila actual de la carta.
    id = create_move("mov1", id_game=1, db=test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.pile == "Deck" == get_move_pile(id, test_db)
    
def test_set_move_pile(test_db, force_teardown):
    
    #Caso 1: Asigna la carta a la mano de un jugador
    id = create_move("mov1", id_game=1, db=test_db)
    set_move_pile(id, "In Hand", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.pile == "In Hand"
    
    #Caso 2: Asigna la carta a la pila de descarte
    set_move_pile(id, "Discard", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.pile == "Discard"
    
    #Caso 3: Asigna la carta al deck
    set_move_pile(id, "Deck", test_db)
    tab = test_db.query(MoveTable).filter_by(id_game=1).first()
    assert tab.pile == "Deck"
    
    #Caso 4: Se asigna a una pila incorrectamente.
    #Falta implementar validacion de las pilas en models.
    
def test_set__move_user(test_db, force_teardown):
    
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