import abc


class Engine:
    """
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self):
        pass

    @abc.abstractproperty
    def engine_name(self):
        pass

    def __repr__(self):
        return f'DBENGINE - {self.engine_name}'

    def __str__(self):
        return f'DBENGINE - {self.engine_name}'

    @abc.abstractmethod
    def list_tables(self):
        pass

    @abc.abstractmethod
    def create(self):
        pass

    @abc.abstractmethod
    def insert(self):
        pass

    @abc.abstractmethod
    def select(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass

    def page(self, table_name, fields=None, where=None, like=None, number=1, limit=1):
        return self.select(table_name=table_name, fields=fields, where=where, like=like, offset=(number - 1) * limit, limit=limit)

    def count(self, table_name, where=None, distinct=None):
        return self.select(
            table_name=table_name,
            fields=[f'COUNT({f"DISTINCT {distinct}" if distinct else "*"})'], where=where, one=True
        )
