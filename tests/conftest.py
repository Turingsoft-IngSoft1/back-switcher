import pytest
from fastapi.testclient import TestClient
from models import DBManager,BoardTable,GameTable,UserTable,MoveTable,FigureTable
from models.base import Base
from main import app

@pytest.fixture(scope='function')
def test_db():
    #Inicializa la base de datos de pruebas.
    bdd_testing = DBManager(testing=True)
    #Session para la Base de datos.
    yield bdd_testing.db
    #Teardown elimina todo registro de la base de datos y cierra la session.
    bdd_testing.teardown()

@pytest.fixture
def client():
    with TestClient(app) as t_client:
        yield t_client

@pytest.fixture(autouse=True)
def mock_server_db(mocker, test_db):
    mocker.patch("router.pre_game.SERVER_DB", test_db)
    mocker.patch("router.game.SERVER_DB", test_db)
    mocker.patch("router.cards.SERVER_DB", test_db)
    # 
    from router.pre_game import SERVER_DB as pre_game_server_db
    from router.game import SERVER_DB as game_server_db
    from router.cards import SERVER_DB as cards_server_db
    #
    assert pre_game_server_db is test_db
    assert game_server_db is test_db
    assert cards_server_db is test_db


@pytest.fixture(scope='function',autouse=True)
def force_teardown(test_db):
    yield
    test_db.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        test_db.execute(table.delete())
    test_db.commit()