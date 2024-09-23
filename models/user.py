from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

# TODO -> Arreglar seguir ejemplo 

class UserTable(Base):
    """Implementacion de la tabla user en la base de datos."""
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    game_id = Column(Integer, ForeignKey('Games.id'), index=True)

    Moves = relationship("FiguresTable",backref="Users")
    Figures = relationship("MovesTable",backref="Users")
