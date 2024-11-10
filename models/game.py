from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from models.base import Base


class GameTable(Base):
    __tablename__ = 'Games'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    state = Column(String, default="Waiting", index=True)
    turn = Column(Integer, default=0, index=True)
    host = Column(Integer, index=True, nullable=False, default=0)
    players = Column(Integer, default=1, index=True)
    min_players = Column(Integer, default=2)
    max_players = Column(Integer, default=4)
    password = Column(String, default="")
    private = Column(Boolean, default=False)
    
    Users = relationship("UserTable", backref="GameTable",cascade="all, delete")
    Boards = relationship("BoardTable", backref="GameTable",cascade="all, delete")
    Moves = relationship("MoveTable", backref="GameTable",cascade="all, delete")
    Figures = relationship("FigureTable", backref="GameTable",cascade="all, delete")