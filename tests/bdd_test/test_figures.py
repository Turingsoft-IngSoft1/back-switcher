import pytest
from querys.figure_queries import *
from models import FigureTable
from sqlite3 import IntegrityError

def test_create_figure(test_db):
    
    #Caso 1: Crear una figura correctamente.
    create_figure("fig01", user_id=1, db=test_db)
    tab = test_db.query(FigureTable).filter_by(user_id=1).first()
    assert tab is not None