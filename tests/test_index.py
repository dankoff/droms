import pytest
from flask import session, request
from app.db import get_db

def test_index(client):
    assert client.get('/').status_code == 200
    with client:
        client.get('/')
        assert 'custIP' in session
        assert session['custIP'] == request.remote_addr

def test_table_selection_available(client, app):
    with client:
        response = client.get('/table_selection/table_4')
        assert session['tableNo'] == 4
        assert response.headers['Location'] == 'http://localhost/menu/'

    with app.app_context():
        res = get_db().execute(
            "select seatsLeft, free from restTable where tableNo=4",
        ).fetchone()
        assert res is not None
        assert res['seatsLeft'] == 3
        assert res['free'] == 1

def test_table_selection_last_seat(client, app):
    response = client.get('/table_selection/table_5')
    assert response.headers['Location'] == 'http://localhost/menu/'
    with app.app_context():
        res = get_db().execute(
            "select seatsLeft, free from restTable where tableNo=5",
        ).fetchone()
        assert res is not None
        assert res['seatsLeft'] == 0
        assert res['free'] == 0

def test_free_seat(client, app):
    assert client.get('/freeseat').status_code == 302
    with client:
        client.get('/table_selection/table_4')
        assert 'tableNo' in session
        response = client.get('/freeseat')
        assert 'tableNo' not in session
        assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        res = get_db().execute(
            "select seatsLeft from restTable where tableNo=4",
        ).fetchone()
        assert res is not None
        assert res['seatsLeft'] == 4
