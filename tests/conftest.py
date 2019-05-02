import os
import tempfile

import pytest
from app import make_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='chef1', password='123456'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

class Order(object):
    def __init__(self, client, app):
        self._client = client
        self._app = app

    def place_order(self):
        self._client.get('/')
        self._client.get('/table_selection/table_4')
        self._client.get('/add_to_cart/item_1')
        self._client.get('/add_to_cart/item_1')
        self._client.get('/add_to_cart/item_2')
        self._client.get('/make_order/total_4.50')

        with self._app.app_context():
            res = get_db().execute(
                "select * from custOrder order by id desc limit 1"
            ).fetchone()
            return res

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def order(client, app):
    return Order(client, app)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = make_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
