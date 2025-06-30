# app/db.py

from flask import g
from app.config import get_db_connection

def get_db():
    if 'db' not in g:
        conn = get_db_connection()
        if conn is not None:
            g.db = conn
            g.db.autocommit = False  # Para tener control de transacciones
        else:
            raise Exception("No se pudo conectar a la base de datos")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
