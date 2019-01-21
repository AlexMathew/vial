import abc

from ..base import Engine


class SQL(Engine):
    """
    """
    __metaclass__ = abc.ABCMeta

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

    def list_tables(self):
        cur = self._conn.cursor()
        cur.execute(self.__class__._tables_query())
        results = [x[0] for x in cur.fetchall()]
        self._conn.commit()
        cur.close()
        return results

    def create(self, table_name, serial=False, fields=None):
        cur = self._conn.cursor()
        cur.execute(self.__class__._create_query(
            table_name=table_name,
            serial=serial,
            fields=fields or {},
        ))
        self._conn.commit()
        cur.close()

    def insert(self, table_name, data=None):
        cur = self._conn.cursor()
        cur.execute(self.__class__._insert_query(table_name, fields=data.keys()), tuple(data.values()))
        self._conn.commit()
        cur.close()
        return True

    def select(self, table_name, fields=None, where=None, like=None, offset=None, limit=None, one=False):
        cur = self._conn.cursor()
        cur.execute(self.__class__._select_query(
            table_name=table_name,
            fields=fields,
            where=where,
            like=like,
            offset=offset,
            limit=limit
        ))
        result = cur.fetchone() if one else cur.fetchall()
        self._conn.commit()
        cur.close()
        return result

    def delete(self, table_name, where=None):
        cur = self._conn.cursor()
        cur.execute(self.__class__._delete_query(table_name, where=where), tuple(where.values()))
        self._conn.commit()
        cur.close()
        return True
