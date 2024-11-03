from pytest import MonkeyPatch


from utils.partial_boards import BoardsManager
from querys import create_game,create_board,get_board

def test_partial_boards(test_db):
    id=create_game("Juego",2,2,test_db)
    create_board(id,test_db)
    partials_boards = BoardsManager()
    partials_boards.initialize(id,test_db)
    board1 = get_board(id,test_db)
    board2 = partials_boards.get(id)
    assert board1 == board2

def test_update_partial_boards(test_db,monkeypatch):
    def mock_shuffle(x):
        pass
    monkeypatch.setattr('models.board.shuffle', mock_shuffle)
    
    id=create_game("Juego1",2,2,test_db)
    create_board(id,test_db)
    partials_boards = BoardsManager()
    partials_boards.initialize(id,test_db)
    board1 = get_board(id,test_db)
    board2 = partials_boards.get(id)
    dif = (0,0)
    for i in range(6):
        for j in range(6):
            if board2[i][j] != board2[0][0]:
                dif = (i,j)
                break

    partials_boards.update(id,(0,0),dif)
    board2 = partials_boards.get(id)
    assert board1 != board2

    aux = board1[0][0] 
    board1[0][0] = board1[dif[0]][dif[1]]
    board1[dif[0]][dif[1]] = aux
    assert board1 == board2

def test_create_multiple_boards(test_db):
    partial_boards = BoardsManager()
    for i in range(50):
        id = create_game(f"Juego{i}",2,2,test_db)
        create_board(id,test_db)
        partial_boards.initialize(id,test_db)
    
    for i in range(50):
        assert get_board(id,test_db) == partial_boards.get(id)

def test_delete_partial_board(test_db):
    partial_boards = BoardsManager()
    id = create_game(f"JuegoN",2,2,test_db)
    create_board(id,test_db)
    partial_boards.initialize(id,test_db)
    partial_boards.remove(id)
    assert partial_boards.get(id) == None

    assert partial_boards.get(404) == None
    partial_boards.remove(404)