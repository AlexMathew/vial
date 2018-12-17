from .field import BaseField, FieldValidationException


class Str(BaseField):
    datatype = 'str'

    def validate(self, value):
        if type(value) is not str:
            raise FieldValidationException("`str` value should be passed")


class Int(BaseField):
    datatype = 'int'

    def validate(self, value):
        if type(value) is not int:
            raise FieldValidationException("`int` value should be passed")


class Float(BaseField):
    datatype = 'float'

    def validate(self, value):
        from decimal import Decimal
        if not type(value) in [float, Decimal]:
            raise FieldValidationException("`float`/`decimal.Decimal` value should be passed")


class Bool(BaseField):
    datatype = 'bool'

    def validate(self, value):
        if value not in [True, False]:
            raise FieldValidationException("`bool` value should be passed")


class Datetime(BaseField):
    datatype = 'datetime'

    def validate(self, value):
        from datetime import datetime
        if not type(value) is datetime:
            raise FieldValidationException("`datetime` value should be passed")
