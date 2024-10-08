from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates

from models.base import Base

valid_moves = tuple([f"mov{i}" for i in range(1,8)])
valid_status = tuple(["Deck", "InHand", "Played", "Discarded"])
class MoveTable(Base):
    """Implementacion de la tabla moves en la base de datos."""
    __tablename__ = "Moves"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="Deck")

    user_id = Column(Integer, ForeignKey('Users.id'))
    id_game = Column(Integer, ForeignKey('Games.id'))
    
    
    @validates('name', 'status')
    def validate(self, key, value):
        if key == 'name':
            if value not in valid_moves:
                raise ValueError('El nombre debe estar dentro de los valores validos')
            else:
                return value
        elif key == 'status':
            if value not in valid_status:
                raise ValueError('El status debe estar dentro de los valores validos')
            else:
                return value