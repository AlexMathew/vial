import abc

from slugify import slugify

from .field import FieldConstrainException, FieldValidationException


class BaseModel:
    __metaclass__ = abc.ABCMeta
    _application = None

    @classmethod
    def use_engine(cls, engine):
        cls._engine = engine

    @classmethod
    def add_application_instance(cls, application):
        cls._application = application

    @classmethod
    def get_table_name(cls):
        return slugify(f'{cls._application.name}_{cls.__name__}').replace('-', '_')

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return f'Model - {self.table_name}'

    def __str__(self):
        return f'Model - {self.table_name}'

    @classmethod
    def get_attributes(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}

    @classmethod
    def serialize_attributes(cls):
        return {k: v.serialize() for k, v in cls.__dict__.items() if not k.startswith('_')}

    @classmethod
    def serialize(cls):
        return {
            'table_name': cls.get_table_name(),
            'fields': cls.serialize_attributes(),
        }

    @classmethod
    def setup(cls):
        with cls._engine as db:
            tables = db.list_tables()
            if cls.get_table_name() not in tables:
                print(f'CREATING TABLE - {cls.get_table_name()}')
                db.create(
                    table_name=cls.get_table_name(),
                    serial=not any([field['primary'] for field in cls.serialize_attributes().values()]),
                    fields=cls.serialize_attributes(),
                )

    @classmethod
    def validate_record(cls, **values):
        if not values:
            raise Exception("Values to be inserted should be passed")

        attributes = cls.get_attributes()

        try:
            for key, val in values.items():
                if key not in attributes:
                    raise Exception(f"Not acceptable key - {key}")
                attributes[key].validate(val)
                if attributes[key].constraint:
                    if not attributes[key].constraint(val):
                        raise FieldConstrainException(f"Constraint failed on key - {key}")

        except FieldValidationException as e:
            raise FieldValidationException(f'{key} - {e}')

    @classmethod
    def insert(cls, **values):
        cls.validate_record(**values)
        attributes = cls.get_attributes()

        for attr, val in attributes.items():
            if attr not in values:
                values[attr] = val.default() if callable(val.default) else val.default

        with cls._engine as db:
            db.insert(table_name=cls.get_table_name(), data=values)

    @classmethod
    def dictify_result(cls, fields, data):
        return {k: v for k, v in zip(fields, data)} if data else {}

    @classmethod
    def get_fields(cls):
        fields = []
        if not any([field['primary'] for field in cls.serialize_attributes().values()]):
            fields.append('id')

        fields.extend(cls.serialize_attributes().keys())

        return fields

    @classmethod
    def get(cls, where=None):
        with cls._engine as db:
            sel = db.select(table_name=cls.get_table_name(), where=where, limit=1, one=True)
            fields = cls.get_fields()
            result = cls.dictify_result(fields=fields, data=sel)

        return result

    @classmethod
    def select(cls, where=None, like=None, offset=None, limit=None):
        with cls._engine as db:
            sels = db.select(table_name=cls.get_table_name(), where=where, like=like, offset=offset, limit=limit)
            fields = cls.get_fields()
            results = [cls.dictify_result(fields=fields, data=sel) for sel in sels]

        return results

    @classmethod
    def page(cls, where=None, like=None, number=1, limit=1):
        with cls._engine as db:
            page_data = db.page(table_name=cls.get_table_name(), where=where, like=like, number=number, limit=limit)
            fields = cls.get_fields()
            results = [cls.dictify_result(fields=fields, data=data) for data in page_data]

        return results

    @classmethod
    def update(cls, where=None, updation=None):
        cls.validate_record(**updation)

        with cls._engine as db:
            db.update(table_name=cls.get_table_name(), where=where, updation=updation)

    @classmethod
    def delete(cls, where=None):
        with cls._engine as db:
            db.delete(table_name=cls.get_table_name(), where=where)
