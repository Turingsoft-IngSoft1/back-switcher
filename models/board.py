import json,random
from random import shuffle

from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class BoardValidationError(Exception):
    """Excepcion para errores del tablero."""
    
    DEFAULT="Exception (BoardValidationError)\n{\n" \
            "1) Solo se permiten los caracteres (R,G,B,Y).\n"\
            "2) El tablero solo puede tener 6 columnas y 6 filas.\n"\
            "3) El tablero debe tener 9 iteraciones de cada caracter permitido.\n}"
    def __init__(self, message: str = DEFAULT):
        super().__init__(message)


class BoardTable(Base):
    __tablename__ = 'Boards'

    id = Column(Integer, primary_key=True, index=True)
    id_game = Column(Integer, ForeignKey('Games.id',ondelete="CASCADE"), unique=True, index=True)
    color = Column(String, default="NOT")
    board = Column(String, index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'board' not in kwargs:
            self.board_json = self.random_distribution()

    @property
    def board_json(self):
        return json.loads(self.board)

    @board_json.setter
    def board_json(self, b_json):

        if not self.validate_board(b_json):
            raise BoardValidationError()
        else:
            self.board = json.dumps(b_json)

    def get_board(self) -> list[list[str]]:
        return self.board_json

    @staticmethod
    def validate_board(board) -> bool :
        
        valid_charset = {'R', 'G', 'B', 'Y'}
        required_count = 9
    
        # Verifica que el tablero tenga 6 filas
        if len(board) != 6:
            return False
        
        # Inicializa un diccionario para contar los colores
        color_counts = {color: 0 for color in valid_charset}
        
        for row in board:
            # Verifica que cada fila tenga 6 columnas
            if len(row) != 6:
                return False
            
            for column in row:
                # Verifica que el carácter sea parte del conjunto válido
                if column not in valid_charset:
                    return False
                
                # Aumenta el contador del color
                color_counts[column] += 1

        # Verifica que cada color tenga exactamente 9 ocurrencias
        for color in valid_charset:
            if color_counts[color] != required_count:
                return False
        
        return True


    @staticmethod
    def random_distribution():
        l = ['R','R','R','R','R','R','R','R','R',
             'G','G','G','G','G','G','G','G','G',
             'B','B','B','B','B','B','B','B','B',
             'Y','Y','Y','Y','Y','Y','Y','Y','Y']
        random.shuffle(l)
        initial_board = []
        for i in range(0, len(l), 6):
            initial_board.append(l[i:i + 6])

        return initial_board
