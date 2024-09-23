from pydantic import BaseModel, Field

class User(BaseModel):
    """Scheme for a user implementation"""
    id: int = Field(description="Unique integer that specifies this user.")
    name: str = Field(min_length=1,max_length=100,description="Name of the user.")
    game: int = Field(description="Unique integer that specifies the current game.")

