from nose import with_setup
from nose.tools import (assert_equal, assert_in, assert_is_none,
                        assert_is_not_none)

from vial.server.application import Application

app = Application('test_runner')


def setup():
    @app.route(methods=['GET'], path='/$')
    def route1():
        return '1'


@with_setup(setup)
def test_application_routes():
    assert_in('get', app._routes)
    assert_is_none(app.validate_route('get', '/'))
    assert_is_not_none(app.validate_route('post', '/'))
    assert_is_not_none(app.validate_route('get', '/1'))
    assert_equal('1', app.get_controller('get', '/')[0]())
