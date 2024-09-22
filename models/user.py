from sqlalchemy import Column, Integer, String
from models.base import Base

# TODO -> Arreglar seguir ejemplo 

class UserTable(Base):
    """Implementacion de la tabla user en la base de datos."""
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    game = Column(Integer, index=True, nullable=False)

