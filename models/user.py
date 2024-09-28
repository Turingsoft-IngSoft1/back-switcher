from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship

class UserTable(Base):
    """Implementacion de la tabla user en la base de datos."""
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    game_id = Column(Integer, ForeignKey('Games.id'), index=True)
    figures_deck = Column(Integer, default=13)

    Moves = relationship("FigureTable",backref="UserTable")
    Figures = relationship("MoveTable",backref="UserTable")