from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class UserTable(Base):
    """Implementacion de la tabla user en la base de datos."""
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    id_game = Column(Integer, ForeignKey('Games.id',ondelete="CASCADE"), index=True)
    figures_deck = Column(Integer, default=12)
    turn = Column(Integer, default=0)

    Moves = relationship("FigureTable", backref="UserTable")
    Figures = relationship("MoveTable", backref="UserTable")
