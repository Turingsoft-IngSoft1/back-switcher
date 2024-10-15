from pydantic import BaseModel, Field, field_validator
from models.figure import figures

class Figure(BaseModel):
    """Schema for figure cards implementation"""
    name: str = Field(min_length=5, max_length=6, description="Unique string that specifies this figure.")

    @field_validator('name')
    def name_is_valid(cls, v: str) -> str:
        """Chequea si el nombre de la figura es valido"""
        if v not in figures:
            raise ValueError("invalid figure name")
        return v

