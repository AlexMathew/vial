from datetime import datetime
from decimal import Decimal

from .field import BaseField, FieldValidationException


class Str(BaseField):
    datatype = 'str'
    accepted_types = [str]


class Int(BaseField):
    datatype = 'int'
    accepted_types = [int]


class Float(BaseField):
    datatype = 'float'
    accepted_types = [float, Decimal]


class Bool(BaseField):
    datatype = 'bool'

    def validate(self, value):
        if value not in [True, False]:
            raise FieldValidationException("`bool` value should be passed")


class Datetime(BaseField):
    datatype = 'datetime'
    accepted_types = [datetime]
