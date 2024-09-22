from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear el motor de la base de datos
engine = create_engine("sqlite:///./database.db")

# Crear la base declarativa
Base = declarative_base()

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
