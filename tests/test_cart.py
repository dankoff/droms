import pytest
from flask import g, session
from app.db import get_db

def test_view_cart(auth, client):
    assert client.get('/view_cart').status_code == 200
    with client:
        response = client.get('/view_cart')
        assert g.user is None

    auth.login()
    with client:
        response = client.get('/view_cart')
        assert g.user is not None
        assert response.headers['Location'] == 'http://localhost/menu/'

def test_add_to_cart(client):
    with client:
        for i in range(3):
            response = client.get('/add_to_cart/item_{}'.format(i+1))
            assert 'cart' in session
            assert len(session['cart']) == i+1
            assert session['cart'][i]['qty'] == 1
        client.get('/add_to_cart/item_1')
        assert len(session['cart']) == 3
        assert session['cart'][0]['qty'] == 2
        assert session['cart'][0]['total_cost'] == 2.00
        assert response.headers['Location'] == 'http://localhost/menu/'

def test_update_cart_empty_cart(client):
    response = client.get('/update_cart/item_1/action_test')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/view_cart'

def test_update_cart_inc(client):
    with client:
        client.get('/add_to_cart/item_1')
        assert session['cart'][0]['qty'] == 1
        assert session['cart'][0]['total_cost'] == 1.00
        client.get('/update_cart/item_1/action_inc')
        assert session['cart'][0]['qty'] == 2
        assert session['cart'][0]['total_cost'] == 2.00

def test_update_cart_dec(client):
    with client:
        client.get('/add_to_cart/item_1')
        client.get('/add_to_cart/item_1')
        assert session['cart'][0]['qty'] == 2
        assert session['cart'][0]['total_cost'] == 2.00
        client.get('/update_cart/item_1/action_dec')
        assert session['cart'][0]['qty'] == 1
        assert session['cart'][0]['total_cost'] == 1.00

def test_update_cart_delete(client):
    with client:
        client.get('/add_to_cart/item_1')
        client.get('/add_to_cart/item_1')
        client.get('/add_to_cart/item_2')
        assert len(session['cart']) == 2
        assert session['cart'][0]['id'] == '1'
        client.get('/update_cart/item_1/action_remove')
        assert len(session['cart']) == 1
        assert session['cart'][0]['id'] == '2'

def test_make_order(client, order, app):
    with client:
        response = client.get('/make_order/total_1.00')
        assert response.headers['Location'] == 'http://localhost/'
        client.get('/')
        client.get('/table_selection/table_5')
        client.get('/add_to_cart/item_1')
        client.get('/add_to_cart/item_1')
        client.get('/add_to_cart/item_2')
        response = client.get('/make_order/total_4.50')
        assert 'cart' not in session
        assert response.headers['Location'] == 'http://localhost/view_cart'

    with app.app_context():
        res = get_db().execute(
            "select totalCost, tableNo from custOrder where id=4"
        ).fetchone()
        assert res is not None
        assert res['totalCost'] == 4.50
        assert res['tableNo'] == 5

        res = get_db().execute(
            "select itemId, quantity from orderDetail where orderId=4"
        ).fetchall()
        assert len(res) == 2
        assert res[0]['itemId'] == 1
        assert res[0]['quantity'] == 2
        assert res[1]['itemId'] == 2
        assert res[1]['quantity'] == 1

def test_view_bill(client, order):
    assert client.get('/view_bill').status_code == 200
    _ = order.place_order()
    _ = order.place_order()
    response = client.get('/view_bill')
    assert '<td>£4.00</td>' in response.get_data(as_text=True)
    assert '<td>£5.00</td>' in response.get_data(as_text=True)
    assert '<span>£9.00</span>' in response.get_data(as_text=True)

def test_pay_bill(client, order, app):
    myOrder = order.place_order()

    assert myOrder['paid'] == 0
    response = client.post(
        '/view_bill', data={'bill_total' : myOrder['totalCost']}
    )
    assert b'Thank you, a member' in response.data

    with app.app_context():
        query = get_db().execute(
            "select paid from custOrder where id=?", (myOrder['id'],)
        ).fetchone()
        assert query is not None
        assert query['paid'] == 1

        query = get_db().execute(
            "select source, message from communication order by id desc limit 1"
        ).fetchone()
        assert query is not None
        assert query['source'] == 'Kitchen'
        assert 'customer from table 4 has requested' in query['message']
