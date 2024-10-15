from pydantic import BaseModel, Field


class Figure(BaseModel):
    """Schema for figure cards implementation"""
    id: int = Field(description="Unique integer that specifies this figure.")
    name: str = Field(min_length=1, max_length=100, description="Name of the figure.")
    id_user: int = Field(description="Unique integer that specifies the owner of the card.")
    id_game: int = Field(description="Unique integer that specifies the game the card is in.")
    status: str = Field(min_length=1, max_length=100, description="Status the card is in (Hidden, Revealed or Discarded).")