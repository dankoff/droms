import pytest
from flask import request
from app.db import get_db
from app.util import save_message

def test_home(client, auth):
    response = client.get('/kitchen/home')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/auth/login'

    auth.login()
    assert client.get('/kitchen/home').status_code == 200

def test_completeOrder(client, auth, order, app):
    auth.login('waiter1', '123456')
    assert client.get('/kitchen/order/complete').status_code == 302
    auth.logout()

    auth.login('manager', '123456')
    assert client.get('/kitchen/order/complete').status_code == 302
    auth.logout()

    myOrder = order.place_order()
    id = myOrder['id']
    assert myOrder['completed'] == 0
    auth.login()
    with client:
        r = client.get(
            '/kitchen/order/complete', query_string={
            'orderId' : id, 'message' : 'Order {} is now ready.'.format(id), \
            'source' : 'TestKitchen'
        })
        json_data = r.get_json()
        assert len(json_data) == 1
        assert json_data[0]['id'] == id
        assert json_data[0]['completed'] == 1

    with app.app_context():
        query = get_db().execute(
            "select completed from custOrder where id=?", (id,)
        ).fetchone()
        assert query is not None
        assert query['completed'] == 1

        query = get_db().execute(
            "select message from communication order by id desc limit 1",
        ).fetchone()
        assert query is not None
        assert 'Order {} is now ready.'.format(id) == query['message']

def test_showOrder(client, auth, order):
    myOrder = order.place_order()
    id = myOrder['id']
    auth.login()
    with client:
        r = client.get(
            '/kitchen/order', query_string={ 'orderId' : id }
        )
        json_data = r.get_json()
        assert len(json_data) == 2
        assert json_data[0]['orderId'] == id
        assert json_data[1]['orderId'] == id
        assert json_data[0]['name'] == 'testItem1'
        assert json_data[0]['quantity'] == 2
        assert json_data[1]['name'] == 'testItem2'
        assert json_data[1]['quantity'] == 1

def test_ordersByDate(client, auth, order):
    ord1 = order.place_order()
    ord2 = order.place_order()
    auth.login()
    with client:
        r = client.get('/kitchen/home/orders')
        json_data = r.get_json()
        assert len(json_data) == 2
        assert json_data[0]['id'] == ord1['id']
        assert json_data[1]['id'] == ord2['id']

def test_message_invalid_user(client, auth):
    auth.login('manager', '123456')
    r = client.get('/kitchen/home/send_message')
    r.status_code == 302
    r.headers['Location'] == 'http://localhost/menu/'

@pytest.mark.parametrize(('username', 'password', 'source'), (
    ('chef1', '123456', 'TestKitchen'),
    ('waiter1', '123456', 'TestBar'),
))
def test_send_message(client, auth, order, app, username, password, source):
    myOrder = order.place_order()
    auth.login(username, password)
    with client:
        r = client.get(
            '/kitchen/home/send_message', query_string={
            'message' : 'test msg', 'source' : source
        })
        json_data = r.get_json()
        assert len(json_data) == 2
        msgs = [ rec['msg'] for rec in json_data ]
        assert 'test msg' in msgs
        assert 'Test Message From {}'.format(source) in msgs

    with app.app_context():
        query = get_db().execute(
            "select message, source from communication order by id desc limit 1",
        ).fetchone()
        assert query is not None
        assert 'test msg' == query['message']
        assert source == query['source']

@pytest.mark.parametrize(('username', 'password', 'source'), (
    ('chef1', '123456', 'TestKitchen'),
    ('waiter1', '123456', 'TestBar'),
))
def test_loadMessages(client, auth, app, username, password, source):
    auth.login(username, password)
    with app.app_context():
        save_message(source, 'test_msg1')
        save_message(source, 'test_msg2')
    with client:
        r = client.get(
            '/kitchen/home/messages', query_string={ 'source' : source }
            )
        json_data = r.get_json()
        assert len(json_data) == 3
        msgs = [ rec['msg'] for rec in json_data ]
        assert 'test_msg1' in msgs
        assert 'test_msg2' in msgs
        assert 'Test Message From {}'.format(source) in msgs
