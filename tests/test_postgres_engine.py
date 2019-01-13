from nose.tools import assert_in
from vial.db.postgresql import Postgresql


def test_create():
    assert_in('id SERIAL PRIMARY KEY', Postgresql._create_query('test', serial=True))
    assert_in(
        'name varchar PRIMARY KEY NOT NULL',
        Postgresql._create_query('test', fields={
            'name': {'type': 'str', 'primary': True, 'not_null': True}
        })
    )


def test_insert():
    assert_in('(name, number)', Postgresql._insert_query('test', fields=['name', 'number']))
    assert_in('(%s, %s)', Postgresql._insert_query('test', fields=['name', 'number']))


def test_select():
    assert_in('SELECT * FROM test', Postgresql._select_query('test'))
    assert_in('name, number', Postgresql._select_query('test', fields=['name', 'number']))
    assert_in("WHERE id=1 AND name='abc'", Postgresql._select_query('test', where={'id': 1, 'name': 'abc'}))
    assert_in('OFFSET 10', Postgresql._select_query('test', offset=10))
    assert_in('LIMIT 10', Postgresql._select_query('test', limit=10))


def test_update():
    assert_in('WHERE id=(%s) AND name=(%s)', Postgresql._update_query('test', where={'id': 1, 'name': 'abc'}))
    assert_in('SET name=(%s), number=(%s)', Postgresql._update_query('test', updation={'name': 'abc', 'number': 123}))


def test_delete():
    assert_in('WHERE id=(%s) AND name=(%s)', Postgresql._delete_query('test', where={'id': 1, 'name': 'abc'}))
