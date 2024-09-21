from sqlalchemy import Column, Integer, String
from models.base import Base, SessionLocal

gameBase = declarative_base()

class Game(Base):
    __tablename__ = 'Games'
    
    id = Column(Integer, primary_key=True, autoIncrement=True)
    name = Column(String)
    state = Column(String, default="Waiting")
    turn = Column(Integer, default=0)
    host = Column(String, foreign_key=True)
    max_players = Column(Integer)
    min_players = Column(Integer)
    password = Column(String, default=None)
    #timer = Column(Integer)
    
def create_game(id: int, 
                name: str, 
                host: str,
                state: str,
                turn: int,
                max_players: int, 
                min_players: int, 
                password: str | None):
    
    db = SessionLocal()
    
    try:
        new_game = Game(id=id, 
                        name=name, 
                        host=host, 
                        max_players=max_players, 
                        min_players=min_players, 
                        password=password)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        print(f"Game {new_game.id} created")
    except Exception as e:
        db.rollback()
        print(f"Error creating game: {e}")
    finally:
        db.close()




"""
    def start_game(self):
        self.state = "Playing"
        #Empezar el timer.
        return self.state
    
    def finish_game(self):
         self.state = "Finished"
         #Parar timer.
         return self.state

    def configure(self, name: str, max_players: int, min_players: int, password: str | None):
        self.max_players = max_players
        self.min_players = min_players
        self.password = password
        self.name = name;
        return self.max_players, self.min_players, self.password
    
    def set_id(self, id: int):
        #Debe garantizar que el ID es único.
        return self.id

    def create_game(self, id: int, name: str, host: str):
        self.id = id
        self.name = name
        self.host = host
        return self.id, self.name, self.host
"""