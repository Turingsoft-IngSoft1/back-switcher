from pydantic import BaseModel, Field


class Move(BaseModel):
    """Schema for move cards implementation"""
    id: int = Field(description="Unique integer that specifies this move.")
    name: str = Field(min_length=1, max_length=100, description="Name of the move.")
    status: str = Field(min_length=1, max_length=100, description="Status the card is in (Deck, InHand, Played or Discarded).")
    user_id: int = Field(description="Unique integer that specifies the owner of the card.")
    id_game: int = Field(description="Unique integer that specifies the game the card is in.")
