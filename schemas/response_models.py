from pydantic import BaseModel, Field
from .game_schema import Game
from .user_schema import User

class ResponseCreate(BaseModel) :
    """Datos obtenidos de crear una partida"""
    id_game: int = Field(ge=0,description="Unique integer that specifies this game.")
    id_player: int = Field(ge=0,description="Unique integer that specifies this player.")

class ResponseJoin(BaseModel) :
    """Datos obtenidos de unirse a una partida"""
    new_player_id: int = Field(ge=0,description="Unique integer that specifies this player.")

class ResponseList(BaseModel) :
    """Datos obtenidos al listar partidas"""
    games_list: list[Game] = Field(description="List of current active games.")

class ResponseUser(BaseModel) :
    """Datos relevantes del usuario"""
    name: str
    id_game: int

class CreateEntry(BaseModel) :
    """Json de entrada para crear partida"""
    game_name: str = Field(min_length=1,max_length=100,description="Unique string that specifies this game.")
    owner_name: str = Field(min_length=1,max_length=100,description="Unique string that specifies this player.")
    min_player: int = Field(ge=2,le=4,description="Game's minimum player number.")
    max_player: int = Field(ge=2,le=4,description="Game's maximum player number.")

class JoinEntry(BaseModel) :
    """Json de entrada para unirse a partida"""
    id_game: int = Field(description="Game's unique ID.")
    player_name: str = Field(min_length=1,max_length=100,description="New player's name.")

class CurrentUsers(BaseModel) :
    """Lista de usuarios conectados"""
    users_list: list[User] = Field(description="Current users in game lobby.")