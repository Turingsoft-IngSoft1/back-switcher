from pydantic import BaseModel, Field

class Game(BaseModel):
    """Scheme for a game implementation
       Example of Field and BaseModel""" #Modificar

    id: int = Field(description="Unique integer that specifies this game.")
    name: str = Field(min_length=1,max_length=100,description="Name of the game.")
