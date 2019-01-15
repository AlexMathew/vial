import sqlite3

from .base import Engine


class Sqlite(Engine):
    """
    """
    engine_name = 'SQLite'
    type_mapping = {
        'int': 'integer',
        'str': 'text',
        'float': 'real',
        'bool': 'integer',
        'date': 'text',
        'time': 'text',
        'datetime': 'text',
        'uuid': 'text',
    }

    def __init__(self, dbname, *args, **kwargs):
        super(Sqlite, self).__init__(*args, **kwargs)
        self.dbname = dbname

    def __enter__(self):
        self._conn = sqlite3.connect(self.dbname)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            try:
                self._conn.commit()
            except Exception as e:
                self._conn.rollback()
                raise e

        else:
            self._conn.rollback()

        self._conn.close()

    @classmethod
    def _tables_query(cls):
        query = ' '.join(f"""
        SELECT name FROM sqlite_master WHERE type='table'
        """.split())
        return query

    def list_tables(self):
        cur = self._conn.cursor()
        cur.execute(Sqlite._tables_query())
        results = [x[0] for x in cur.fetchall()]
        self._conn.commit()
        cur.close()
        return results
