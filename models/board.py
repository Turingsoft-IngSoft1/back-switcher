from sqlalchemy import Column, Integer, String, ForeignKey

from models.base import Base


class BoardTable(Base):
    __tablename__ = 'Board'

    id = Column(Integer, ForeignKey('Game.id'), primary_key=True, index=True)
    color = Column(String, default="NONE")
    cells = Column(list, default=[])
