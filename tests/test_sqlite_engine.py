from nose.tools import assert_in
from vial.db.sql.sqlite import Sqlite


def test_create():
    assert_in('id INTEGER PRIMARY KEY AUTOINCREMENT', Sqlite._create_query('test', serial=True))
    assert_in(
        'name text PRIMARY KEY NOT NULL',
        Sqlite._create_query('test', fields={
            'name': {'type': 'str', 'primary': True, 'not_null': True}
        })
    )


def test_insert():
    assert_in('(name, number)', Sqlite._insert_query('test', fields=['name', 'number']))
    assert_in('(?, ?)', Sqlite._insert_query('test', fields=['name', 'number']))


def test_select():
    assert_in('SELECT * FROM test', Sqlite._select_query('test'))
    assert_in('name, number', Sqlite._select_query('test', fields=['name', 'number']))
    assert_in("WHERE id=1 AND name='abc'", Sqlite._select_query('test', where={'id': 1, 'name': 'abc'}))
    assert_in('OFFSET 10', Sqlite._select_query('test', offset=10))
    assert_in('LIMIT 10', Sqlite._select_query('test', limit=10))


def test_update():
    assert_in('WHERE id=(?) AND name=(?)', Sqlite._update_query('test', where={'id': 1, 'name': 'abc'}))
    assert_in('SET name=(?), number=(?)', Sqlite._update_query('test', updation={'name': 'abc', 'number': 123}))


def test_delete():
    assert_in('WHERE id=(?) AND name=(?)', Sqlite._delete_query('test', where={'id': 1, 'name': 'abc'}))
