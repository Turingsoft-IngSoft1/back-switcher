from pydantic import BaseModel, Field

class User(BaseModel):
    """Scheme for a user implementation
       Example of Field and BaseModel""" #Modificar
    id: int = Field(description="Unique integer that specifies this user.")
    name: str = Field(min_length=1,max_length=100,description="Name of the user.")

