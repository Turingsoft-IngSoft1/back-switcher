from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import tempfile

# Crear la base declarativa
Base = declarative_base()

def get_engine(testing=False):
    """Devuelve el motor de la base de datos que se usara."""
    if testing:
        temp_file = tempfile.NamedTemporaryFile(suffix='.db',delete=False)
        return create_engine(f"sqlite:///{temp_file.name}.db")
    else:
        return create_engine("sqlite:///./database.db", pool_size=50, max_overflow=200)

class DBManager:
    def __init__(self,testing=False):
        self.engine = get_engine(testing=testing)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=self.engine)
        self.db = self.SessionLocal()

    def teardown(self):
        with self.db.begin():
            for table in Base.metadata.tables.values():
                self.db.execute(table.delete())
        self.db.commit()
        self.db.close()

    def close(self):
        self.db.close()