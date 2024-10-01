from querys import game_queries


def testGameCreation():
    """Test para la creación de partida y las demás queries"""
    game_id1 = game_queries.create_game("LaPartida1", "Luciano", 2, 4)
    game_id2 = game_queries.create_game("LaPartida2", "Valentin", 2, 3)
    game_id3 = game_queries.create_game("LaPartida3", "Nahuel", 2, 2)

    print("Partida1 original: " + str(game_queries.get_game(game_id1)))
    print("\n")
    game_queries.set_game_state(game_id1, "Playing")
    game_queries.set_game_turn(game_id1, 3)
    print("Partida1 modificada: " + str(game_queries.get_game(game_id1)))

    print("Partida2 original: " + str(game_queries.get_game(game_id2)))
    print("\n")
    game_queries.set_game_state(game_id2, "Finished")
    game_queries.set_game_turn(game_id2, 2)
    print("Partida2 modificada: " + str(game_queries.get_game(game_id2)))
    print("\n")
    print("Partida 3 original: " + str(game_queries.get_game(game_id3)))
