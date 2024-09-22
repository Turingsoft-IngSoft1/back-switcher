from sqlalchemy import Column, Integer, String
from models.base import Base

class GameTable(Base):
    
    __tablename__ = 'Games'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    state = Column(String, default="Waiting", index=True)
    turn = Column(Integer, default=0, index=True)
    host = Column(String, index=True, nullable=False)
    players = Column(Integer, default=1, index=True)
    max_players = Column(Integer, default=4)
    min_players = Column(Integer, default=2)
    password = Column(String, default=None)