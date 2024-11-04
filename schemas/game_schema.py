from pydantic import BaseModel, Field


class Game(BaseModel):
    id: int = Field(description="Unique integer that specifies this game.")
    name: str = Field(min_length=1, max_length=100, description="Name of the game.")
    state: str = Field(min_length=1, max_length=100, description="State of the game. (Waiting, Playing, or Finished)")
    turn: int = Field(description="Integer that specifies the actual turn of the game.")
    host: int = Field(description="Host of the game's ID.")
    players: int = Field(description="Number of players that have joined the game)")
    max_players: int = Field(description="Maximum number of players that can join the game.")
    min_players: int = Field(description="Minimum number of players that can join the game.")
    password: str = Field(min_length=1, max_length=60, description="Password of the game.")
