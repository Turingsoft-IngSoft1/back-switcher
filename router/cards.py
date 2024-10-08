from fastapi import APIRouter

cards = APIRouter()


@cards.get("/get_moves")
def get_moves(id_player: int, id_game: int):
    """Obtener cartas de movimiento."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # TODO Implementacion ->

    return {"Movimientos Entregados Correctamente."}


@cards.post("/use_moves")
def use_moves(id_player: int, id_game: int):
    """Usar una carta de movimiento."""

    # TODO Implementacion ->

    return {"Movimientos Usados Correctamente."}


@cards.get("/get_figure")
def get_figure(id_player: int, id_game: int):
    """Obtener cartas de figura."""

    # En caso de exito debe de modificar el estado del jugador dandole nuevas cartas y sacando estas de las disponibles.

    # TODO Implementacion ->

    return {"Figuras Entregadas Correctamente."}


@cards.post("/use_figure")
def use_figure(id_player: int, id_game: int):
    """Usar una carta de figura."""

    # TODO Implementacion ->

    return {"Figuras Usadas Correctamente."}
