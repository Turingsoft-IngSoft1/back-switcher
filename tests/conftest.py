import pytest
from models import DBManager,BoardTable,GameTable,UserTable,MoveTable,FigureTable

@pytest.fixture(scope='session')
def test_db():
    #Inicializa la base de datos de pruebas.
    TEST = DBManager(testing=True)
    #Session para la Base de datos.
    yield TEST.db

    #Teardown elimina todo registro de la base de datos, close cierra la session.
    TEST.teardown()
    TEST.close()