import abc


class BaseField:
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def datatype(self):
        pass

    @abc.abstractproperty
    def accepted_types(self):
        pass

    def __init__(self, primary=False, not_null=False, unique=False, default=None, constraint=None, *args, **kwargs):
        self.primary = primary
        self.not_null = not_null
        self.unique = unique
        self.default = default
        self.constraint = constraint

    def __repr__(self):
        return f'{self.datatype} - PRIMARY:{self.primary} - NOT_NULL:{self.not_null}'

    def __str__(self):
        return f'{self.datatype} - PRIMARY:{self.primary} - NOT_NULL:{self.not_null}'

    def serialize(self):
        return {
            'type': self.datatype,
            'primary': self.primary,
            'not_null': self.not_null,
            'unique': self.unique,
        }

    def validate(self, value):
        if isinstance(value, tuple(self.accepted_types)):
            raise FieldValidationException(f"Value should be of type {self.accepted_types}")


class FieldValidationException(Exception):
    def __init__(self, *args, **kwargs):
        super(FieldValidationException, self).__init__(*args, **kwargs)


class FieldConstrainException(Exception):
    def __init__(self, *args, **kwargs):
        super(FieldConstrainException, self).__init__(*args, **kwargs)
