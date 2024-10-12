import pytest
from querys import create_board,get_board,get_color,update_board
from models import BoardTable
from sqlite3 import IntegrityError

def test_create_board(test_db,force_teardown):
    
    #Caso 1: Crear un tablero correctamente.
    create_board(id_game=1,db=test_db)
    tab = test_db.query(BoardTable).filter_by(id_game=1).first()
    assert tab is not None
    
    #Caso 2: Intentar introducir el mismo id_game.
    try:
        create_board(id_game=1, db=test_db)
    except IntegrityError:
        #Deberia ocurrir un rollback
        pass
    count = test_db.query(BoardTable).count()
    assert count == 1

def test_get_color(test_db,force_teardown):

    #Color no se puede modificar todavia.
    create_board(id_game=1,db=test_db)
    tab = test_db.query(BoardTable).filter_by(id_game=1).first()
    assert tab.color == "NOT" == get_color(1,test_db)

def test_get_board(test_db,force_teardown):

    #Comprobar que los board del metodo y de la tabla son iguales.
    create_board(id_game=1,db=test_db)
    tab = test_db.query(BoardTable).filter_by(id_game=1).first()
    assert comp_boards(tab.get_board(), get_board(1,test_db))

def test_update_board(test_db,force_teardown):
    #Caso 0:
    sucess=[['R','R','R','R','R','R'],
            ['R','R','R','G','G','G'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]

    #Caso 1: Tratando de insertar colores imposibles.
    error1=[['Z','R','R','R','R','R'],
            ['R','Z','R','G','G','G'],
            ['G','G','Z','G','G','G'],
            ['B','B','B','Z','B','B'],
            ['B','B','B','Y','Z','Y'],
            ['Y','Y','Y','Y','Y','Z']]
    
    #Caso 2: No hay la misma cantidad de (R,G,B,Y).
    error2=[['R','R','R','R','R','R'],
            ['R','R','R','R','R','R'],
            ['G','G','G','G','G','G'],
            ['B','B','B','B','B','B'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    #Caso 3: No es un tablero valido de 6x6.
    error3=[['R','R','R','R','R','R','R'],
            ['R','R','R','R','R','R','G'],
            ['G','G','G','G','G','G','B'],
            ['B','B','B','B','B','B','Y'],
            ['B','B','B','Y','Y','Y'],
            ['Y','Y','Y','Y','Y','Y']]
    
    #C0
    create_board(id_game=1,db=test_db)
    update_board(1,sucess,test_db)
    assert comp_boards(sucess, get_board(1,test_db))
    

    #C1: Deberia hacer rollback cuando intenta updatear.
    create_board(id_game=2,db=test_db)
    update_board(2,error1,test_db)
    assert not comp_boards(error1, get_board(2,test_db))

    #C2: Deberia hacer rollback cuando intenta updatear.
    create_board(id_game=3,db=test_db)
    update_board(3,error2,test_db)
    assert not comp_boards(error1, get_board(3,test_db))

    #C3: Deberia hacer rollback cuando intenta updatear.
    create_board(id_game=4,db=test_db)
    update_board(4,error3,test_db)
    assert not comp_boards(error1, get_board(4,test_db))


@staticmethod
def comp_boards(b1: list[list[str]], b2: list[list[str]]):
    for row1,row2 in zip(b1,b2):
        if len(row1) != len(row2):
            return False
        for col1,col2 in zip(row1,row2):
            if col1 != col2:
                return False

    return True 