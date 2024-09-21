from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from game_queries import *
from database import SessionLocal, engine  # Assuming you have a database.py for session and engine setup
from models import Base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Game(BaseModel):
    
    id: int = Field(description="Unique integer that specifies this game.")
    name: str = Field(min_length=1,max_length=100,description="Name of the game.")
    state: str = Field(min_length=1,max_length=100,description="State of the game. (Waiting, Playing, or Finished)")
    turn: int = Field(description="Integer that specifies the actual turn of the game.")
    host: str = Field(min_length=1,max_length=100,description="Name of the host of the game.")
    max_players: int = Field(description="Maximum number of players that can join the game.")
    min_players: int = Field(description="Minimum number of players that can join the game.")
    password: str | None = Field(min_length=1,max_length=100,description="Password of the game.")
    timer: int | None = Field(description="Time in seconds since the beginning of the match.")


