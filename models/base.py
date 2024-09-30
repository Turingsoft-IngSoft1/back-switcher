from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# Crear el motor de la base de datos
engine = create_engine("sqlite:///./database.db")

# Crear la base declarativa
Base = declarative_base()

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

class DBManager:
    def __init__(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def teardown(self):
        with self.db.begin() :
            for table in Base.metadata.tables.values():
                self.db.execute(table.delete())
        self.db.commit()
        self.db.close()

