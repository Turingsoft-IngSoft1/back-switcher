import pytest
from schemas.move_schema import Move
from models.move import valid_moves

def test_create_move():
    # Test de creación con nomnbre y posición inicial válida
    move = Move(name="mov1", initial_position=[2, 2])
    assert (move.name == "mov1") and (move.initial_position==(2,2))

    # Test de creación con nombre inválido
    with pytest.raises(ValueError):
        Move(name="invalid_move", initial_position=[0, 0])
    
    # Test de creación con posición inicial inválida
    with pytest.raises(ValueError):
        Move(name="mov1", initial_position=[-1, 7])
    
    # Test de creación con valores válidos
    for m in valid_moves:
        move = Move(name=m, initial_position=[2, 2])
        assert len(move.available_moves) == 4

def test_move_available_moves_center():
    # Test de movimientos disponibles con posicion inicial en el centro.
    move1 = Move(name="mov1", initial_position=[2, 2])
    expected_moves = [(4, 4), (4, 0), (0, 4), (0, 0)]
    assert set(move1.available_moves) == set(expected_moves)
    
    move2 = Move(name="mov2", initial_position=[2, 2])
    expected_moves = [(4, 2), (2, 4), (2, 0), (0, 2)]
    assert set(move2.available_moves) == set(expected_moves)

    move3 = Move(name="mov3", initial_position=[2, 2])
    expected_moves = [(1, 2), (3, 2), (2, 1), (2, 3)]
    assert set(move3.available_moves) == set(expected_moves)

    move4 = Move(name="mov4", initial_position=[2, 2])
    expected_moves = [(3, 3), (1, 1), (1, 3), (3, 1)]
    assert set(move4.available_moves) == set(expected_moves)
    
    move5 = Move(name="mov5", initial_position=[2, 2])
    expected_moves = [(3, 0), (4, 3), (1, 4), (0, 1)]
    assert set(move5.available_moves) == set(expected_moves)

    move6 = Move(name="mov6", initial_position=[2, 2])
    expected_moves = [(1, 0), (4, 1), (3, 4), (0, 3)]
    assert set(move6.available_moves) == set(expected_moves)

    move7 = Move(name="mov7", initial_position=[2, 2])
    expected_moves = [(5, 2), (0, 2), (2, 5), (2, 0)]
    assert set(move7.available_moves) == set(expected_moves)

def test_move_available_moves_corner():
    # Test de movimientos disponibles con posicion inicial en una esquina.
    move1 = Move(name="mov1", initial_position=[0, 0])
    expected_moves = [(2, 2)]
    assert set(move1.available_moves) == set(expected_moves)
    
    move2 = Move(name="mov2", initial_position=[0, 0])
    expected_moves = [(0, 2), (2, 0)]
    assert set(move2.available_moves) == set(expected_moves)

    move3 = Move(name="mov3", initial_position=[0, 0])
    expected_moves = [(0, 1), (1, 0)]
    assert set(move3.available_moves) == set(expected_moves)

    move4 = Move(name="mov4", initial_position=[0,0])
    expected_moves = [(1, 1)]
    assert set(move4.available_moves) == set(expected_moves)
    
    move5 = Move(name="mov5", initial_position=[0,0])
    expected_moves = [(2, 1)]
    assert set(move5.available_moves) == set(expected_moves)

    move6 = Move(name="mov6", initial_position=[0,0])
    expected_moves = [(1, 2)]
    assert set(move6.available_moves) == set(expected_moves)
    
    move7 = Move(name="mov7", initial_position=[0, 0])
    expected_moves = [(5, 0), (0, 0), (0, 5)]
    assert set(move7.available_moves) == set(expected_moves)