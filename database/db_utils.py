import sqlite3


def get_connection_to_db(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    return con
