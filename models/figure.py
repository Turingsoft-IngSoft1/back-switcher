from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint

from models.base import Base

figures = tuple([f"fige{i:02d}" for i in range(1,8)]+[f"fig{i:02d}" for i in range(1,19)])
valid_status = tuple(["Hidden","Revealed", "Discarded"])

class FigureTable(Base):
    """Implementacion de la tabla figures en la base de datos."""
    __tablename__ = "Figures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    id_game = Column(Integer, ForeignKey('Games.id', ondelete="CASCADE"))
    id_user = Column(Integer, ForeignKey('Users.id'))
    status = Column(String, default="Hidden")
    
    __table_args__ = (
        CheckConstraint(f"name IN {figures}", name="valid_name_check"),
        CheckConstraint(f"status IN {valid_status}", name="valid_status_check")
    )