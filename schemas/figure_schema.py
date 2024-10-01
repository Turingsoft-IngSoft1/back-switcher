from pydantic import BaseModel, Field


class Move(BaseModel):
    """Schema for figure cards implementation"""
    id: int = Field(description="Unique integer that specifies this figure.")
    name: str = Field(min_length=1, max_length=100, description="Name of the figure.")
    user_id: int = Field(description="Unique integer that specifies the owner of the card.")
