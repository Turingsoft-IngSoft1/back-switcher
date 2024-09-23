from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class FigureTable(Base):
    """Implementacion de la tabla figures en la base de datos."""
    __tablename__ = "Figures"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    user_id = Column(Integer, ForeignKey('Users.id'))