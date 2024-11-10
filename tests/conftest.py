import pytest
from fastapi.testclient import TestClient
from models import DBManager,BoardTable,GameTable,UserTable,MoveTable,FigureTable
from models.base import Base
from utils.partial_boards import BoardsManager
from main import app

@pytest.fixture(scope='function')
def test_db():
    #Inicializa la base de datos de pruebas.
    bdd_testing = DBManager(testing=True)
    #Session para la Base de datos.
    yield bdd_testing.db
    #Teardown elimina todo registro de la base de datos y cierra la session.
    bdd_testing.teardown()

@pytest.fixture(autouse=True,scope='function')
def partial_boards():
    boards = BoardsManager()
    yield boards

@pytest.fixture
def client():
    with TestClient(app) as t_client:
        yield t_client

@pytest.fixture(autouse=True)
def mock_server_db(mocker, test_db, partial_boards):
    mocker.patch("router.pre_game.SERVER_DB", test_db)
    mocker.patch("router.game.SERVER_DB", test_db)
    mocker.patch("router.cards.SERVER_DB", test_db)
    mocker.patch('utils.partial_boards.PARTIAL_BOARDS',partial_boards)
    # 
    from router.pre_game import SERVER_DB as pre_game_server_db
    from router.game import SERVER_DB as game_server_db
    from router.cards import SERVER_DB as cards_server_db
    from utils.partial_boards import PARTIAL_BOARDS as p_boards
    #
    assert pre_game_server_db is test_db
    assert game_server_db is test_db
    assert cards_server_db is test_db
    assert p_boards  is partial_boards