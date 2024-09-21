from fastapi import APIRouter,HTTPException
from schemas import game_schema
from querys import game_queries
from sqlalchemy.orm import Session
from models import SessionLocal, engine  
from models import Base  # Assuming your models are in a file named models.py
from schemas import game_schema

game = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Chequear HTTPExceptions y Completar con el comentario (""" """) para la posterior documentacion.

@game.post("/leave_game")
def leave(id_player: int, id_game: int) :
    """Abandonar Partida."""
    #En caso de exito debe avisarle al front el id del jugador que abandono y actualizar el estado de la partida.
    #Debe avisar al resto de jugadores por WebSockets ?

    # TODO Implementacion ->

    return {"Exit Successful."}

@game.post("/skip_turn")
def skip(id_player: int, id_game: int) :
    """Pasar el turno."""

    #En caso de exito debe saltear el turno y actualizar la partida para los demas jugadores.

    # TODO Implementacion ->

    return {"Skip Successful."}

@game.get("/game_status")
def get_status(id_player: int, id_game: int) :
    """Consultar estado de partida/turnos."""
    game = game_queries.get_game_status(db, id_game)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

def get_host(id_game: int):
    """Consultar quién es el host del juego."""
    host = game_queries.get_game_host(db, id_game)
    return host

def get_max_players(id_game: int):
    """Consultar la cantidad máxima de jugadores."""
    max_players = game_queries.get_game_max_players(db, id_game)
    return max_players

def get_min_players(id_game: int):
    """Consultar la cantidad mínima de jugadores."""
    min_players = game_queries.get_game_min_players(db, id_game)
    return min_players

def get_password(id_game: int):
    """Consultar la contraseña del juego."""
    password = game_queries.get_game_password(db, id_game)
    return password

def get_turn(id_game: int):
    """Consultar el turno actual."""
    turn = game_queries.get_game_turn(db, id_game)
    return turn


@game.get("/board_status")
def get_board(id_player: int, id_game: int) :
    """Consultar estado del tablero."""

    # TODO Implementacion ->

    return {"Board Status."}