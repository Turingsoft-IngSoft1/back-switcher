from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from models.base import Base
from models.user import UserTable

class FiguresTable(Base):
    """Implementacion de la tabla figures en la base de datos."""
    __tablename__ = "Figures"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    user_id = Column(Integer, ForeignKey('Users.id'))
    
    user: Mapped["UserTable"] = relationship("UserTable", back_populates="Figures")