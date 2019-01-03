import enum
import os
from datetime import datetime
from hashlib import md5
from random import random

from vial.db.postgresql import Postgresql
from vial.orm import types
from vial.orm.model import BaseModel

engine = Postgresql(
    dbname=os.getenv('POSTGRES_DATABASE'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)


def create_auth_token():
    return md5(str(random()).encode('utf-8')).hexdigest()


class User(BaseModel):
    _engine = engine

    email = types.Str(not_null=True, unique=True)
    password = types.Str(not_null=True)
    maintainer = types.Bool(default=False)
    auth_token = types.Str(not_null=True, default=create_auth_token, unique=True)


class CategoryChoices(enum.Enum):
    CATEGORY_A = 1
    CATEGORY_B = 2
    CATEGORY_C = 3


class Product(BaseModel):
    _engine = engine

    code = types.Str(not_null=True, primary=True)
    name = types.Str(not_null=True)
    description = types.Str()
    category = types.Int(constraint=lambda val: val in [x.value for x in list(CategoryChoices)])
    created_date = types.Datetime(default=datetime.now)
