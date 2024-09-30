from querys import board_queries


def testBoardCreation():
    """Test para la creación de tablero y las demás queries"""

    board_id1 = board_queries.create_board(1)
    board_id2 = board_queries.create_board(2)
    board_id3 = board_queries.create_board(3)
    print("Tablero1 original: " + str(board_queries.get_board(board_id1)))
    print("\n")
    board_queries.modify_cell(board_id1, 1, "Rojo")
    print("Tablero1 modificado: " + str(board_queries.get_board(board_id1)))
    print("\n")
    print("Tablero2 original: " + str(board_queries.get_board(board_id2)))
    print("\n")
    board_queries.modify_cell(board_id2, 2, "Azul")
    print("Tablero2 modificada: " + str(board_queries.get_board(board_id2)))
    print("\n")
    print("Tablero3 original: " + str(board_queries.get_board(board_id3)))
    print("\n")
    board_queries.modify_cell(board_id3, 3, "Verde")
    print("Tablero3 modificada: " + str(board_queries.get_board(board_id3)))
    print("\n")
    print("Color bloqueado de tablero1: " + str(board_queries.get_color(board_id1)))
    print("\n")
    print("Color bloqueado de tablero2: " + str(board_queries.get_color(board_id2)))
    print("\n")
    print("Color bloqueado de tablero3: " + str(board_queries.get_color(board_id3)))
