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

    def create_table(self, table_name: str, fields: dict[str, str]):
        self._execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(f'{key} {value}' for key, value in fields.items())})
        """)

    def add(self, table_name: str, data: dict[str, t.Any]):
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())
        self._execute(f"""INSERT INTO {table_name} ({column_names})
                          VALUES ({placeholders})""",
                      column_values)

    def delete(self, table_name: str, criteria: dict[str, t.Any]):
        delete_criteria = ' AND '.join(f'{field} = ?' for field in criteria)
        self._execute(f"""DELETE FROM {table_name} WHERE {delete_criteria}""",
                      tuple(criteria.values()))

    def select(self, table_name: str,
               criteria: t.Optional[dict[str, t.Any]] = None,
               order_by_clause: t.Optional[str] = None):
        criteria = criteria or {}
        query = [f'SELECT * FROM {table_name}']
        if criteria:
            select_criteria ='WHERE ' + ' AND '.join(f'{field} = ?' for field in criteria)
            query.append(select_criteria)
        if order_by_clause:
            order_criteria = f'ORDER BY {order_by_clause}'
            query.append(order_criteria)
        return self._execute(' '.join(query), tuple(criteria.values()))

    def update(self, table_name: str,
               upd_fields: dict[str, t.Any],
               criteria: t.Optional[dict[str, t.Any]] = None):
        criteria = criteria or {}
        set_criteria = ' AND '.join(f'{field} = ?' for field in upd_fields)
        query = [f'UPDATE {table_name} SET {set_criteria}']
        if criteria:
            update_criteria ='WHERE ' + ' AND '.join(f'{field} = ?' for field in criteria)
            query.append(update_criteria)
        self._execute(' '.join(query), (*upd_fields.values(), *criteria.values()))


    def __del__(self):
        self.connection.close()
