from models import move
from schemas import move_schema
from querys import move_queries

def test_create_move():
    move1 = move_queries.create_move("Cruce en linea")
    move2 = move_queries.create_move("Cruce en linea con espacio")
    move3 = move_queries.create_move("Cruce en 'L' a la derecha con dos espacios")
    
    print(f"Movimiento 1: {move_queries.get_move_name(move1)}")
    print(f"Movimiento 2: {move_queries.get_move_name(move2)}")
    print(f"Movimiento 3: {move_queries.get_move_name(move3)}")
    
    pile1 = move_queries.get_move_pile(move1)
    pile2 = move_queries.get_move_pile(move2)
    pile3 = move_queries.get_move_pile(move3)
    
    print(f"Pila de movimiento 1: {pile1}")
    print(f"Pila de movimiento 2: {pile2}")
    print(f"Pila de movimiento 3: {pile3}")
    
    pile1 = move_queries.set_move_pile(move1, "In Hand")
    pile2 = move_queries.set_move_pile(move2, "Discard")
    pile3 = move_queries.set_move_pile(move3, "In Hand")
    
    print(f"Pila de movimiento 1 actualizada: {move_queries.get_move_pile(move1)}")
    print(f"Pila de movimiento 2 actualizada: {move_queries.get_move_pile(move2)}")
    print(f"Pila de movimiento 3 actualizada: {move_queries.get_move_pile(move3)}")
    
    user1 = move_queries.get_users(move1)
    user2 = move_queries.get_users(move2)
    user3 = move_queries.get_users(move3)
    
    print(f"Dueño movimiento 1: {user1}")
    print(f"Dueño movimiento 2: {user2}")
    print(f"Dueño movimiento 3: {user3}")
    
    user1 = move_queries.set_users(move1, 123413414)
    user2 = move_queries.set_users(move2, 4134100)
    user3 = move_queries.set_users(move3, 79879800718)
    
    print(f"Dueño movimiento 1 actualizado: {move_queries.get_users(move1)}")
    print(f"Dueño movimiento 2 actualizado: {move_queries.get_users(move2)}")
    print(f"Dueño movimiento 3 actualizado: {move_queries.get_users(move3)}")
    
    move_queries.remove_move(move1)
    move_queries.remove_move(move2)
    move_queries.remove_move(move3)