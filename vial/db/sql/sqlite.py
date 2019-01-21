import sqlite3

from .base import SQL


class Sqlite(SQL):
    """
    """
    engine_name = 'SQLite'
    type_mapping = {
        'int': 'integer',
        'str': 'text',
        'float': 'real',
        'bool': 'integer',
        'date': 'date',
        'time': 'timestamp',
        'datetime': 'timestamp',
        'uuid': 'text',
    }

    def __init__(self, dbname, *args, **kwargs):
        super(Sqlite, self).__init__(*args, **kwargs)
        self.dbname = dbname if dbname.endswith('.sqlite3') else ''.join([dbname, '.sqlite3'])

    def __enter__(self):
        self._conn = sqlite3.connect(self.dbname)
        return self

    @classmethod
    def _tables_query(cls):
        query = ' '.join(f"""
        SELECT name FROM sqlite_master WHERE type='table'
        """.split())
        return query

    @classmethod
    def _create_query(cls, table_name, serial=False, fields=None):
        fields = fields or {}
        query = ' '.join(f"""
        CREATE TABLE {table_name}
        ( {'id INTEGER PRIMARY KEY AUTOINCREMENT' if serial else ''}
        {', ' if serial and fields else ''}
        {' , '.join([
            f'''{k}
            {Sqlite.type_mapping.get(v.get('type', 'str'))}
            {' PRIMARY KEY' if v.get('primary') else ''}
            {' NOT NULL' if v.get('not_null') else ''}
            {' UNIQUE' if v.get('unique') else ''}''' for k, v in fields.items()
        ])});
        """.split())
        return query

    @classmethod
    def _insert_query(cls, table_name, fields=None):
        fields = fields or ()
        query = ' '.join(f"""
        INSERT INTO {table_name} ({', '.join(fields)})
        VALUES ({', '.join(["?" for _ in fields])})
        """.split())
        return query

    @classmethod
    def _select_query(cls, table_name, fields=None, where=None, like=None, offset=None, limit=None):
        def stringify(v, like=False):
            if like:
                return f"'%{v}%'"
            return f"'{v}'"

        query = ' '.join(f"""
        SELECT {', '.join(fields) if fields else '*'} FROM {table_name}
        {f' WHERE {" AND ".join([f"{k}={v if isinstance(v, (int, float, bool)) else stringify(v)}" for k, v in where.items()])}' if where else ''}
        {f' {"AND" if where else "WHERE"} {" AND ".join([f"{k} LIKE {stringify(v, like=True)}" for k, v in like.items()])}' if like else ''}
        {f' LIMIT {limit}' if limit else ''}
        {f' OFFSET {offset}' if offset else ''};
        """.split())
        return query

    @classmethod
    def _update_query(cls, table_name, where=None, updation=None):
        query = ' '.join(f"""
        UPDATE {table_name}
        {f' SET {", ".join([f"{k}=(?)" for k in updation.keys()])}' if updation else ''}
        {f' WHERE {" AND ".join([f"{k}=(?)" for k in where.keys()])}' if where else ''}
        """.split())
        return query

    def update(self, table_name, where=None, updation=None):
        cur = self._conn.cursor()
        cur.execute(Sqlite._update_query(
            table_name, where=where, updation=updation
        ), (tuple(updation.values()) + tuple(where.values())))
        self._conn.commit()
        cur.close()
        return True

    @classmethod
    def _delete_query(cls, table_name, where=None):
        query = ' '.join(f"""
        DELETE FROM {table_name}
        {f' WHERE {" AND ".join([f"{k}=(?)" for k in where.keys()])}' if where else ''}
        """.split())
        return query
