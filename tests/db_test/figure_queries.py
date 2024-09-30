from querys import figure_queries


def test_figure_queries():
    figure1 = figure_queries.create_figure("L", 5134123513)
    figure2 = figure_queries.create_figure("Mini T", 4124814)
    figure3 = figure_queries.create_figure("Mini L", 12300123)

    print(f"Figura 1: {figure_queries.get_figure_name(figure1)}")
    print(f"Figura 2: {figure_queries.get_figure_name(figure2)}")
    print(f"Figura 3: {figure_queries.get_figure_name(figure3)}")

    user1 = figure_queries.get_users(figure1)
    user2 = figure_queries.get_users(figure2)
    user3 = figure_queries.get_users(figure3)

    print(f"Dueño figura 1: {user1}")
    print(f"Dueño figura 2: {user2}")
    print(f"Dueño figura 3: {user3}")

    figure_queries.remove_figure(figure1)
    figure_queries.remove_figure(figure2)
    figure_queries.remove_figure(figure3)
