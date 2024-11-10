from models.game import GameTable
from models.user import UserTable
from models.board import BoardTable
from models.move import MoveTable
from models.figure import FigureTable
from models.base import DBManager

#Base de datos por defecto del servidor.
SERVER = DBManager()
SERVER_DB = SERVER.db