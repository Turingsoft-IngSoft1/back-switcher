from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from models.base import Base
from models.moves import MovesTable
from models.figures import FiguresTable

class UserTable(Base):
    """Implementacion de la tabla user en la base de datos."""
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game = Column(Integer, nullable=False)
    turn = Column(Integer)
    figure_deck = Column(Integer, default=13)
    
    moves: Mapped[list[MovesTable]] = relationship("Moves", back_populates="Users")
    figures: Mapped[list[FiguresTable]] = relationship("Figures", back_populates="Users")

