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

def test_move_available_moves():
    # Test de movimientos disponibles
    move = Move(name="mov1", initial_position=[2, 2])
    expected_moves = [(4, 4), (4, 0), (0, 4), (0, 0)]
    assert set(move.available_moves) == set(expected_moves)
    
    move = Move(name="mov2", initial_position=[2, 2])
    expected_moves = [(4, 2), (2, 4), (2, 0), (0, 2)]
    assert set(move.available_moves) == set(expected_moves)

    move = Move(name="mov3", initial_position=[2, 2])
    expected_moves = [(1, 2), (3, 2), (2, 1), (2, 3)]
    assert set(move.available_moves) == set(expected_moves)

    move = Move(name="mov4", initial_position=[2, 2])
    expected_moves = [(3, 3), (1, 1), (1, 3), (3, 1)]
    assert set(move.available_moves) == set(expected_moves)
    
    move = Move(name="mov5", initial_position=[2, 2])
    expected_moves = [(3, 0), (4, 3), (1, 4), (0, 1)]
    #assert set(move.available_moves) == set(expected_moves)

    move = Move(name="mov6", initial_position=[2, 2])
    expected_moves = [(4, 1), (3, 0), (0, 3), (3, 0)]
    assert set(move.available_moves) == set(expected_moves)