from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.base import Base
from models.user import UserTable

class MovesTable(Base):
    """Implementacion de la tabla moves en la base de datos."""
    __tablename__ = "Moves"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pile = Column(String, default="Deck")
    quantity = Column(Integer)
    
    user_id = Column(Integer, ForeignKey('Users.id'))
    
    user: Mapped["UserTable"] = relationship("UserTable", back_populates="Moves")