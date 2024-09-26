from typing import List
from pydantic import BaseModel, Field
from .game_schema import Game

class ResponseCreate(BaseModel) :
    """Datos obtenidos de crear una partida"""
    id_game: int = Field(ge=0,description="Unique integer that specifies this game.")
    id_player: int = Field(ge=0,description="Unique integer that specifies this player.")

class ResponseJoin(BaseModel) :
    """Datos obtenidos de unirse a una partida"""
    new_player_id: int = Field(ge=0,description="Unique integer that specifies this player.")

class ResponseList(BaseModel) :
    """Datos obtenidos al listar partidas"""
    games_list: List[Game] = Field(description="List of current active games.")
