import typing as t
from db_utils import get_connection_to_db


class DatabaseManager:

    def __init__(self, db_path: str) -> None:
        self.connection = get_connection_to_db(db_path)

    def _execute(self, sql_statement: str, data: t.Optional[t.Iterable[t.Any]] = None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql_statement, data or [])
            return cursor

    def create_table(self, table_name, fields):
        self._execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(f'{key} {value}' for key, value in fields.items())})
        """)

    def add(self, table_name, data):
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())
        self._execute(f"""INSERT INTO {table_name} ({column_names})
                          VALUES ({placeholders})""",
                      column_values)

    def delete(self, table_name, criteria):
        delete_criteria = ' AND '.join(f'{key}=?' for key in criteria.keys())
        self._execute(f"""DELETE FROM {table_name} WHERE {delete_criteria}""",
                      tuple(criteria.values()))

    def __del__(self):
        self.connection.close()
