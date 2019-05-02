import pytest
from flask import g, session
from app.db import get_db

@pytest.mark.parametrize(('username', 'password', 'id', 'type'), (
    ('chef1', '123456', 2, 'Cook'),
    ('waiter1', '123456', 3, 'Waiter'),
    ('manager', '123456', 1, 'Manager')
))
def test_login(client, auth, username, password, id, type):
    assert client.get('/auth/login').status_code == 200
    response = auth.login(username, password)
    assert response.headers['Location'] == 'http://localhost/kitchen/home'

    with client:
        client.get('/')
        assert session['user_id'] == id
        assert g.user['username'] == username
        assert g.user['type'] == type
        assert 'tableNo' not in session

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('chef1', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_login_already_logged_in(auth, client):
    auth.login()
    with client:
        response = client.get('/auth/login')
        assert g.user is not None
        assert response.headers['Location'] == 'http://localhost/kitchen/home'

def test_login_with_table_selected(auth, client):
    with client:
        client.get('/table_selection/table_4')
        assert session['tableNo'] == 4
        auth.login()
        assert 'tableNo' not in session

def test_register_no_user(client):
    with client:
        response = client.get('/auth/register')
        assert g.user is None
        assert 'http://localhost/auth/login' == response.headers['Location']

def test_register_user_not_manager(auth, client):
    auth.login()
    with client:
        response = client.get('/auth/register')
        assert g.user['type'] != 'Manager'
        assert 'http://localhost/kitchen/home' == response.headers['Location']

def test_register(auth, client, app):
    auth.login('manager', '123456')
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'chef2', 'password': 'test123', \
        'confPassword' : 'test123', 'staffType' : 'Cook', 'workPlace' : 'Kitchen'}
    )
    assert 'http://localhost/kitchen/home' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from staff where username = 'chef2'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'confPass',
    'staffType', 'workPlace', 'message'), (
    ('abc', '123', '123', '', '', b'Password must be at least 6 characters long.'),
    ('abc', '123456', '123455', '', '', b'Passwords must match.'),
    ('chef1', 'abcdefg', 'abcdefg', '', '', b'already registered'),
))
def test_register_validate_input(auth, client, username, password, confPass,
                                    staffType, workPlace, message):
    auth.login('manager', '123456')
    response = client.post(
        '/auth/register', data={'username': username, 'password': password, \
        'confPassword' : confPass, 'staffType' : staffType, \
        'workPlace' : workPlace}
    )
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        response = auth.logout()
        assert 'user_id' not in session
        assert response.headers['Location'] == 'http://localhost/auth/login'
