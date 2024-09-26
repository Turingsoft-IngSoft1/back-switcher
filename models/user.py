from sqlalchemy import Column, Integer, String
from models.base import Base,SessionLocal

# TODO -> Arreglar seguir ejemplo 

class User(Base):
    """Implementacion de la tabla user en la base de datos."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

def create_user(name: str):
    """Crear un usuario y agregarlo."""
    db = SessionLocal()
    try:
        new_user = User(name=name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User {new_user.name} created")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
