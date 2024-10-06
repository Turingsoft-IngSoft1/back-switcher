import json,random
from random import shuffle

from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base


class BoardTable(Base):
    __tablename__ = 'Boards'

    id = Column(Integer, primary_key=True, index=True)
    id_game = Column(Integer, ForeignKey('Games.id'), unique=True, nullable=False, index=True)
    color = Column(String, default="N")
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

        if self.validate_board(b_json):
            self.board = json.dumps(b_json)

    def get_board(self) -> list[list[str]]:
        return self.board_json

    @staticmethod
    def validate_board(board) -> bool :
        valid_charset = {'R','G','B','Y'}
        if len(board) != 6:
            return False
        for row in board:
            if len(row) != 6:
                return False
            for column in row:
                if column not in valid_charset:
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
