from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates

from models.base import Base

easy_figures = tuple([f"fige{i:02d}" for i in range(1,8)])
hard_figures = tuple([f"fig{i:02d}" for i in range(1,19)])
class FigureTable(Base):
    """Implementacion de la tabla figures en la base de datos."""
    __tablename__ = "Figures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    user_id = Column(Integer, ForeignKey('Users.id'))

    @validates('name')
    def validate_name(self, key, value):
        if key == 'name':
            if value not in (easy_figures+hard_figures):
                raise ValueError('El nombre debe estar dentro de los valores validos')
            else:
                return value