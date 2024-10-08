from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import validates

from models.base import Base

valid_moves = tuple([f"mov{i}" for i in range(1,8)])
valid_status = tuple(["Deck", "InHand", "Played", "Discarded"])
class MoveTable(Base):
    """Implementacion de la tabla moves en la base de datos."""
    __tablename__ = "Moves"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, default="Deck", index=True)

    user_id = Column(Integer, ForeignKey('Users.id'))
    id_game = Column(Integer, ForeignKey('Games.id'))
    
    __table_args__ = (
        CheckConstraint(f"status IN {valid_status}", name="valid_status_check"),
        CheckConstraint(f"name IN {valid_moves}", name="valid_name_check")
    )
    
