from nose.tools import assert_in
from vial.db.postgresql import Postgresql

pg = Postgresql(dbname='', user='', password='', host='', port='')


def test_create():
    assert_in('id SERIAL PRIMARY KEY', pg._create_query('test', serial=True))
    assert_in(
        'name varchar PRIMARY KEY NOT NULL',
        pg._create_query('test', fields={
            'name': {'type': 'str', 'primary': True, 'not_null': True}
        })
    )


def test_insert():
    assert_in('(name, number)', pg._insert_query('test', fields=['name', 'number']))
    assert_in('(%s, %s)', pg._insert_query('test', fields=['name', 'number']))


def test_select():
    assert_in('SELECT * FROM test', pg._select_query('test'))
    assert_in('name, number', pg._select_query('test', fields=['name', 'number']))
    assert_in("WHERE id=1 AND name='abc'", pg._select_query('test', where={'id': 1, 'name': 'abc'}))
    assert_in('OFFSET 10', pg._select_query('test', offset=10))
    assert_in('LIMIT 10', pg._select_query('test', limit=10))


def test_update():
    assert_in('WHERE id=(%s) AND name=(%s)', pg._update_query('test', where={'id': 1, 'name': 'abc'}))
    assert_in('SET name=(%s), number=(%s)', pg._update_query('test', updation={'name': 'abc', 'number': 123}))


def test_delete():
    assert_in('WHERE id=(%s) AND name=(%s)', pg._delete_query('test', where={'id': 1, 'name': 'abc'}))
