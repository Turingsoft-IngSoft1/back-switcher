from models import move
from schemas import move_schema
from querys import move_queries

def test_create_move():
    move1 = move_queries.create_move("Cruce en linea", 5134123513)
    move2 = move_queries.create_move("Cruce en linea con espacio", 4124814)
    move3 = move_queries.create_move("Cruce en 'L' a la derecha con dos espacios", 12300123)
    
    print(f"Movimiento 1: {move_queries.get_move_name(move1)}")
    print(f"Movimiento 2: {move_queries.get_move_name(move2)}")
    print(f"Movimiento 3: {move_queries.get_move_name(move3)}")
    
    pile1 = move_queries.get_move_pile(move1)
    pile2 = move_queries.get_move_pile(move2)
    pile3 = move_queries.get_move_pile(move3)
    
    print(f"Pila de movimiento 1: {pile1}")
    print(f"Pila de movimiento 2: {pile2}")
    print(f"Pila de movimiento 3: {pile3}")
    
    pile1 = move_queries.set_move_pile(move1)
    pile2 = move_queries.set_move_pile(move2)
    pile3 = move_queries.set_move_pile(move3)
    
    print(f"Pila de movimiento 1 actualizada: {pile1}")
    print(f"Pila de movimiento 2 actualizada: {pile2}")
    print(f"Pila de movimiento 3 actualizada: {pile3}")
    
    user1 = move_queries.get_users(move1)
    user2 = move_queries.get_users(move2)
    user3 = move_queries.get_users(move3)
    
    print(f"Dueño movimiento 1: {user1}")
    print(f"Dueño movimiento 2: {user2}")
    print(f"Dueño movimiento 3: {user3}")
    
    move_queries.remove_move(move1)
    move_queries.remove_move(move2)
    move_queries.remove_move(move3)