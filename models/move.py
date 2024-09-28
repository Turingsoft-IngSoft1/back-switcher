from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class MoveTable(Base):
    """Implementacion de la tabla moves en la base de datos."""
    __tablename__ = "Moves"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pile = Column(String, default="Deck")

    user_id = Column(Integer, ForeignKey('Users.id'))