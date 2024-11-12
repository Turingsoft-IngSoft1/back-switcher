import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from models import DBManager
from models.base import Base
from utils.partial_boards import BoardsManager
from utils.profiles import ProfilesManager
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

@pytest.fixture(autouse=True,scope='function')
def profiles_testing():
    profiles = ProfilesManager()
    yield profiles

@pytest.fixture
def client():
    with TestClient(app) as t_client:
        yield t_client

@pytest.fixture(autouse=True)
def mock_asynctimer(mocker):
    # Mockear las funciones `start_timer` y `restart_timer` para que no hagan nada
    mocker.patch('router.pre_game.start_timer', new_callable=AsyncMock)
    mocker.patch('router.pre_game.restart_timer', new_callable=AsyncMock)
    mocker.patch('router.game.start_timer', new_callable=AsyncMock)

@pytest.fixture(autouse=True)
def mock_timer(mocker):
    def my_mock(x):
        pass
    mocker.patch('router.pre_game.initialize_timer', my_mock)
    mocker.patch('router.game.remove_timer', my_mock)

@pytest.fixture(autouse=True)
def mock_server_db(mocker, test_db, partial_boards, profiles_testing):
    mocker.patch("router.pre_game.SERVER_DB", test_db)
    mocker.patch("router.game.SERVER_DB", test_db)
    mocker.patch("router.cards.SERVER_DB", test_db)
    mocker.patch('utils.partial_boards.PARTIAL_BOARDS', partial_boards)
    mocker.patch('utils.profiles.PROFILES', profiles_testing)
    # 
    from router.pre_game import SERVER_DB as pre_game_server_db
    from router.game import SERVER_DB as game_server_db
    from router.cards import SERVER_DB as cards_server_db
    from utils.partial_boards import PARTIAL_BOARDS as p_boards
    from utils.profiles import PROFILES as real_profiles
    #
    assert pre_game_server_db is test_db
    assert game_server_db is test_db
    assert cards_server_db is test_db
    assert p_boards  is partial_boards
    assert real_profiles is profiles_testing
