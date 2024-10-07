from sqlalchemy import Column, Integer, String
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
    password = Column(String, default="password")
    moves_deck = Column(Integer, default=49)
    Users = relationship("UserTable", backref="GameTable")
    Moves = relationship("MoveTable", backref="GameTable")
    # Boards = relationship("Board", backref="GameTable")
