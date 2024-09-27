from pydantic import BaseModel, Field

class Move(BaseModel):
    """Schema for move cards implementation"""
    id: int = Field(description="Unique integer that specifies this move.")
    name: str = Field(min_length=1,max_length=100,description="Name of the move.")
    pile: str = Field(min_length=1,max_length=100,description="Pile the card is in (Deck or Discard).")
    user_id: int = Field(description="Unique integer that specifies the owner of the card.")