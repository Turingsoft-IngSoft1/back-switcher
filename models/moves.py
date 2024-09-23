from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class MovesTable(Base):
    """Implementacion de la tabla moves en la base de datos."""
    __tablename__ = "Moves"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pile = Column(String, default="Deck")
    quantity = Column(Integer)

    user_id = Column(Integer, ForeignKey('Users.id'))