import sqlite3
import os

__cnx = None
def get_sql_connection():
    global __cnx
    if __cnx is None:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(base_dir, 'database.db')
        cnx = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
        cnx.row_factory = sqlite3.Row 
    return cnx

