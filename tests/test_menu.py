import pytest
from app.db import get_db

def test_menu_display(client):
    response = client.get('/menu/')
    assert response.status_code == 200
    for i in range(3):
        assert 'testItem{}'.format(i+1) in response.get_data(as_text=True)
        assert 'testItem{}Desc'.format(i+1) in response.get_data(as_text=True)
        assert 'testSection{}'.format(i+1) in response.get_data(as_text=True)

@pytest.mark.parametrize(('filters', 'itemNames'), (
    (['Vegetarian'], ['testItem1', 'testItem2', 'testItem3']),
    (['Vegan'], ['testItem2', 'testItem1', 'testItem3']),
    (['Mild'], ['testItem1', 'testItem2', 'testItem3'])
))
def test_menu_filters_single(client, filters, itemNames):
    data = { 'filters' : filters }
    response = client.post(
        '/menu/', data=data
    )
    assert itemNames[0] in response.get_data(as_text=True)
    assert itemNames[1] not in response.get_data(as_text=True)
    assert itemNames[2] not in response.get_data(as_text=True)

def test_menu_filter_multiple(client):
    data = { 'filters' : ['Vegetarian', 'Hot'] }
    response = client.post(
        '/menu/', data=data
    )
    assert b'testItem1' in response.data
    assert b'testItem3' in response.data
    assert b'testItem2' not in response.data

def test_menu_filter_empty(client):
    data = { 'filters' : [] }
    response = client.post(
        '/menu/', data=data
    )
    assert b'testItem1' in response.data
    assert b'testItem3' in response.data
    assert b'testItem2' in response.data

@pytest.mark.parametrize(('url', 'data', 'query'), (
    ('/menu/create_menu', { 'name' : 'menu1', 'description' : '', \
     'restaurant' : 'testRestaurant' }, \
     "select * from menu where name = 'menu1'"),
    ('/menu/testMenu1/add_section', {'name' : 'section1', 'description' : '' },\
     "select * from section where name = 'section1'"),
    ('/menu/testMenu1/add_item', {'name' : 'item1', 'description' : 'desc', \
     'cost' : 5.50, 'section' : 'testSection1', 'diet' : '', 'spicy' : ''}, \
     "select * from item where name='item1'")
))
def test_create_stuff(client, auth, app, url, data, query):
    assert client.get(url).headers['Location'] == \
    'http://localhost/auth/login'

    auth.login()
    assert client.get(url).headers['Location'] == \
    'http://localhost/menu/'
    auth.logout()

    auth.login('manager', '123456')
    assert client.get(url).status_code == 200
    response = client.post(
        url, data=data
    )
    assert response.headers['Location'] == 'http://localhost/menu/'

    with app.app_context():
        assert get_db().execute(
            query,
        ).fetchone() is not None

def test_edit_section(client, auth, app):
    auth.login('manager', '123456')
    assert client.get('/menu/testMenu1/edit_section').status_code == 200
    response = client.post(
        '/menu/testMenu1/edit_section', data={'name' : 'testSection2', \
        'description' : 'testDesc', 'section' : 'testSection2', \
        'action' : 'Save'}
    )
    assert response.headers['Location'] == 'http://localhost/menu/'

    with app.app_context():
        query = get_db().execute(
            "select description from section where name='testSection2'",
        ).fetchone()
        assert query is not None
        assert query['description'] == 'testDesc'

def test_delete_section(client, auth, app):
    auth.login('manager', '123456')
    response = client.post(
        '/menu/testMenu1/edit_section', data={'name' : '', \
        'description' : '', 'section' : 'testSection2', \
        'action' : 'Delete'}
    )
    assert response.headers['Location'] == 'http://localhost/menu/'

    with app.app_context():
        assert get_db().execute(
            "select * from section where name='testSection2'",
        ).fetchone() is None

        assert len(get_db().execute(
            "select * from item where section='testSection2'",
        ).fetchall()) == 0

def test_edit_item(client, auth, app):
    auth.login('manager', '123456')
    assert client.get('/menu/testMenu1/edit_item').status_code == 200
    response = client.post(
        '/menu/testMenu1/edit_item', data={'item' : '1', \
        'name' : 'testItem1', 'description' : 'newDesc', \
        'cost' : 7.00, 'section' : 'testSection1', \
        'diet' : '', 'spicy' : '', 'action' : 'Save' }
    )
    assert response.headers['Location'] == 'http://localhost/menu/'

    with app.app_context():
        query = get_db().execute(
            "select description, cost from item where id='1'",
        ).fetchone()
        assert query is not None
        assert query['description'] == 'newDesc'
        assert query['cost'] == 7.00

def test_delete_item(client, auth, app):
    auth.login('manager', '123456')
    response = client.post(
        '/menu/testMenu1/edit_item', data={'item' : '1', \
        'name' : '', 'description' : '', \
        'cost' : 0.00, 'section' : '', \
        'diet' : '', 'spicy' : '', 'action' : 'Delete' }
    )
    assert response.headers['Location'] == 'http://localhost/menu/'

    with app.app_context():
        assert get_db().execute(
            "select * from item where id='1'",
        ).fetchone() is None
